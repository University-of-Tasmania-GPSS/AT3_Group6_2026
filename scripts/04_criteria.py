"""Criteria for the trail suitability models.

Each criterion scores every 10 m cell from 0 (bad for a track) to 1 (ideal).
Constraints are cells a track cannot use (1 = excluded).

Run from the cheyne_trail folder: python scripts/04_criteria.py
"""
import os

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from scipy.ndimage import distance_transform_edt

# Vegetation score for each TASVEG group
VEG_SCORES = {
    "Dry eucalypt forest and woodland": 0.9,
    "Native grassland": 0.8,
    "Modified land": 1.0,
    "Other natural environments": 0.7,
    "Wet eucalypt forest and woodland": 0.6,
    "Non eucalypt forest and woodland": 0.6,
    "Moorland sedgeland and rushland": 0.5,
    "Highland treeless vegetation": 0.4,
    "Rainforest and related scrub": 0.4,
    "Scrub heathland and coastal complexes": 0.3,
    "Saltmarsh and wetland": 0.2,
}

# Communities scored differently from the rest of their group
VEG_CODE_SCORES = {
    "HCH": 0.1,  # alpine coniferous heathland
    "NLM": 0.2,  # swamp forest
}

# Communities a track must avoid: threatened communities listed in
# Schedule 3A of the Nature Conservation Act 2002, plus open water
VEG_EXCLUDED = [
    "RPF", "RPP", "RPW",  # pencil pine (Athrotaxis cupressoides)
    "RKP", "RKS", "RKF",  # King Billy pine (Athrotaxis selaginoides)
    "ASP",                # Sphagnum peatland
    "HCM",                # cushion moorland
    "GPH",                # highland Poa grassland
    "MGH",                # highland grassy sedgeland
    "MDS",                # subalpine Diplarrena latifolia rushland
    "OAQ",                # open water
]

# Buttongrass moorland communities (wet, peaty ground)
BUTTONGRASS = ["MBE", "MBW", "MBS", "MBR"]

# The 10 m grid every raster is built on
dem = rasterio.open("data/processed/dem_10m.tif")
shape = dem.shape
transform = dem.transform
slope = rasterio.open("data/processed/slope_deg.tif").read(1)

# Vector data
veg = gpd.read_file("data/raw/list/tasveg.gpkg")
hydro_lines = gpd.read_file("data/raw/list/hydro_lines.gpkg")
hydro_areas = gpd.read_file("data/raw/list/hydro_areas.gpkg")
transport = gpd.read_file("data/raw/list/transport.gpkg")

# --- Criteria ---

# Slope: 1 up to 10 degrees, falling to 0 at 30 degrees
slope_score = np.clip((30 - slope) / (30 - 10), 0, 1)

# Vegetation: group score, replaced by the community score where one is set
veg["score"] = veg["VEG_GROUP"].map(VEG_SCORES)
veg["score"] = veg["VEGCODE"].map(VEG_CODE_SCORES).fillna(veg["score"])
veg_score = rasterize(zip(veg.geometry, veg["score"]), out_shape=shape, transform=transform,
                      fill=np.nan, dtype="float32")

# Streams: 0 within 30 m of a stream, rising to 1 at 100 m
streams = pd.concat([
    hydro_lines[hydro_lines["HYDLNTY1"] == "Watercourse"],
    hydro_areas[hydro_areas["HYDARTY1"] == "Watercourse"],
])
stream_cells = rasterize(streams.geometry, out_shape=shape, transform=transform)
stream_distance = distance_transform_edt(stream_cells == 0) * 10  # metres
stream_score = np.clip((stream_distance - 30) / (100 - 30), 0, 1)

# Wetland: 0.1 in mapped swamps and wet areas, 0.4 in buttongrass moorland, 1 elsewhere
wetlands = hydro_areas[hydro_areas["HYDARTY1"] == "Wetland"]
wetland_cells = rasterize(wetlands.geometry, out_shape=shape, transform=transform)
buttongrass = veg[veg["VEGCODE"].isin(BUTTONGRASS)]
buttongrass_cells = rasterize(buttongrass.geometry, out_shape=shape, transform=transform)
wetland_score = np.where(buttongrass_cells == 1, 0.4, 1)
wetland_score = np.where(wetland_cells == 1, 0.1, wetland_score)

# Access: 1 on a road or track, falling to 0 at 5 km away
access = transport[transport["TRANS_TYPE"].isin(["Road", "Track"])]
access_cells = rasterize(access.geometry, out_shape=shape, transform=transform)
access_distance = distance_transform_edt(access_cells == 0) * 10  # metres
access_score = np.clip(1 - access_distance / 5000, 0, 1)

# --- Constraints ---

lakes = hydro_areas[hydro_areas["HYDARTY1"] == "Water Body"]
lake_cells = rasterize(lakes.geometry, out_shape=shape, transform=transform)

excluded_veg = veg[veg["VEGCODE"].isin(VEG_EXCLUDED)]
excluded_veg_cells = rasterize(excluded_veg.geometry, out_shape=shape, transform=transform)

steep = slope > 35

constraints = (lake_cells == 1) | (excluded_veg_cells == 1) | steep

# --- Save ---

criteria = {
    "slope": slope_score,
    "vegetation": veg_score,
    "streams": stream_score,
    "wetland": wetland_score,
    "access": access_score,
}
os.makedirs("data/processed/criteria", exist_ok=True)
profile = dem.profile  # float32 with NaN as no-data, same grid as the DEM
for name, score in criteria.items():
    with rasterio.open(f"data/processed/criteria/{name}.tif", "w", **profile) as dst:
        dst.write(score.astype("float32"), 1)

profile.update(dtype="uint8", nodata=None)
with rasterio.open("data/processed/constraints.tif", "w", **profile) as dst:
    dst.write(constraints.astype("uint8"), 1)

print(f"Excluded by constraints: {constraints.mean():.1%} of the study area")

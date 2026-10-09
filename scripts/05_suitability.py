"""Suitability surfaces from the criteria, using two decision rules.

1. AHP: pairwise comparisons give the weight of each criterion.
2. WLC: weighted sum of the criteria.
3. TOPSIS: how close each cell is to the best possible cell,
   relative to the worst possible cell.

Both rules use the same criteria and weights. Constraint cells are set to NaN.

Run from the cheyne_trail folder: python scripts/05_suitability.py
"""
import numpy as np
import rasterio

NAMES = ["slope", "vegetation", "streams", "wetland", "access"]

# AHP pairwise comparison matrix (Saaty 1-9 scale): how much more important
# the row criterion is than the column criterion
AHP = np.array([
    # slope  veg  streams wetland access
    [1,      2,   3,      3,      5],  # slope
    [1/2,    1,   2,      2,      4],  # vegetation
    [1/3,    1/2, 1,      1,      3],  # streams
    [1/3,    1/2, 1,      1,      3],  # wetland
    [1/5,    1/4, 1/3,    1/3,    1],  # access
])

# --- AHP weights ---

# Weights are the principal eigenvector of the matrix, scaled to sum to 1
values, vectors = np.linalg.eig(AHP)
i = np.argmax(values.real)
weights = vectors[:, i].real
weights = weights / weights.sum()

# Consistency ratio: should be below 0.10 (Saaty 1980)
n = len(NAMES)
consistency_index = (values[i].real - n) / (n - 1)
consistency_ratio = consistency_index / 1.12  # 1.12 = random index for 5 criteria

for name, weight in zip(NAMES, weights):
    print(f"{name}: {weight:.3f}")
print(f"Consistency ratio: {consistency_ratio:.3f}")

# --- Load criteria and constraints ---

criteria = [rasterio.open(f"data/processed/criteria/{name}.tif").read(1) for name in NAMES]
constraints = rasterio.open("data/processed/constraints.tif").read(1)
allowed = constraints == 0

# --- WLC: weighted sum ---

wlc = sum(weight * criterion for weight, criterion in zip(weights, criteria))

# --- TOPSIS ---

# Criteria are already scaled 0-1, so they are only weighted (no extra normalisation)
weighted = [weight * criterion for weight, criterion in zip(weights, criteria)]

# Distance from each cell to the best and worst value of every weighted criterion
distance_to_best = np.sqrt(sum((w - w[allowed].max()) ** 2 for w in weighted))
distance_to_worst = np.sqrt(sum((w - w[allowed].min()) ** 2 for w in weighted))
topsis = distance_to_worst / (distance_to_best + distance_to_worst)

# --- Save, with constraint cells as NaN ---

wlc[~allowed] = np.nan
topsis[~allowed] = np.nan

profile = rasterio.open("data/processed/dem_10m.tif").profile  # float32, NaN as no-data
with rasterio.open("data/processed/suitability_wlc.tif", "w", **profile) as dst:
    dst.write(wlc.astype("float32"), 1)
with rasterio.open("data/processed/suitability_topsis.tif", "w", **profile) as dst:
    dst.write(topsis.astype("float32"), 1)

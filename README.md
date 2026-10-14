# Trail through the Cheyne Range

Modelling a new walking track along the Cheyne Range, Tasmania, using multi-criteria suitability modelling, anisotropic movement-cost modelling and path optimisation.

KGG375 GIS Project (AT3) – Group 6 – University of Tasmania, 2026

## Jupyter Book

📖 [View the published Jupyter Book](https://university-of-tasmania-gpss.github.io/AT3_Group6_2026/)

## Group members

- Gabriel Pham
- Sanden Cook

## Objectives

**Aim:** To model and compare optimal routes for a new walking track along the Cheyne Range by weighing environmental factors that affect where a track should go.

1. Develop and compare two suitability models for a walking track using different decision rules (WLC and TOPSIS), with criteria weights from the Analytic Hierarchy Process (AHP).
2. Implement an anisotropic (direction-dependent) movement-cost model that accounts for the different effort of uphill and downhill walking.
3. Generate and compare routes from different start points using a least-cost path algorithm.
4. Compare and visualise the routes using maps, elevation profiles and route statistics.

## Repository structure

| Path | Contents |
|---|---|
| `index.md`, `methods.md`, `results.md`, `discussion.md`, `conclusion.md` | The Jupyter Book pages (Introduction, Methods, Results, Discussion, Conclusion) |
| `dem_3d.html` | Interactive 3D view of the DEM, embedded on the Introduction page |
| `scripts/04_criteria.py` | Builds the five suitability criteria (0–1) and the constraint mask |
| `scripts/05_suitability.py` | AHP weights, then WLC and TOPSIS suitability surfaces |
| `walking_cost.ipynb` | Slope and aspect (WhiteboxTools), direction-aware movement cost and Dijkstra least-cost routes |
| `data/raw/list/` | LIST vector data: TASVEG 5.0, hydrographic lines and areas, transport segments |
| `data/raw/points/` | Start/end access points and summits (created in ArcGIS Pro) |
| `data/processed/` | 10 m DEM, slope, the constraint mask (`constraints.tif`) and the WLC and TOPSIS suitability rasters |
| `data/processed/criteria/` | The five standardised criteria rasters (slope, vegetation, streams, wetland, access) |
| `environment.yml` | Conda environment for running the scripts and notebooks |

All spatial data is in GDA2020 / MGA Zone 55 (EPSG:7855) on a 10 m grid.

## Data sources

- **DEM:** 1 m DEM (Land Tasmania / theLIST), aggregated to 10 m. The original file (~730 MB) is too large for GitHub and is not included; the 10 m version used in the analysis is in `data/processed/`.
- **TASVEG 5.0, LIST Hydrographic Lines and Areas, LIST Transport Segments:** theLIST open data service, © State of Tasmania (CC BY 3.0 AU).

## How to reproduce the analysis

1. Create the Python environment (includes WhiteboxTools, used in `walking_cost.ipynb`):
   ```
   conda env create -f environment.yml
   conda activate kgg375
   ```
2. From the repository folder, run the scripts in order:
   ```
   python scripts/04_criteria.py
   python scripts/05_suitability.py
   ```
   `04_criteria.py` recreates `data/processed/criteria/` and `constraints.tif`, which `05_suitability.py` needs. Copies of these outputs are already included in the repository.
3. Open `walking_cost.ipynb`, choose the suitability raster and the start, end (and optional middle) points, then run all cells. Each least-cost route is saved as a GeoTIFF (route cells = 1).
4. To preview the Jupyter Book locally:
   ```
   jupyter book start
   ```
   then open http://localhost:3000. Pushing to `main` rebuilds and republishes the website automatically.

## AI usage

   Claude was used as a coding assistant during this project. It was used to:
   - help write and debug the Python scripts 
   - fix bugs and memory problems in the least-cost path notebook 
   - help create figures and give feedback on code structure

   All analysis decisions (study area, criteria, AHP comparisons, start points and route choices) were made by the group, and all AI output was reviewed, tested and edited before use.
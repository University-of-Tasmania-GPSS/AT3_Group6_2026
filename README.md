# Trail through the Cheyne Range

Modelling a new walking track along the Cheyne Range, Tasmania, using multi-criteria suitability modelling, anisotropic movement-cost modelling and path optimisation.

KGG375 GIS Project (AT3) – Group 6 – University of Tasmania, 2026

## Jupyter Book

📖 [View the published Jupyter Book](LINK-TO-BE-ADDED)

## Group members

- Gabriel Pham
- Sanden Cook

## Objectives

**Aim:** To model and compare optimal routes for a new walking track along the Cheyne Range by weighing environmental factors that affect where a track should go.

1. Develop and compare two suitability models for a walking track using different decision rules (WLC and TOPSIS), with criteria weights from the Analytic Hierarchy Process (AHP).
2. Implement an anisotropic movement-cost model (Tobler's hiking function) that accounts for the different effort of uphill and downhill walking.
3. Generate and compare routes from different start points using a least-cost path algorithm.
4. Compare and visualise the routes using maps, elevation profiles and route statistics.

## Repository structure

| Path | Contents |
|---|---|
| `jupyter_book.ipynb` | The project write-up (Jupyter Book source) |
| `scripts/04_criteria.py` | Builds the five suitability criteria (0–1) and the constraint mask |
| `scripts/05_suitability.py` | AHP weights, then WLC and TOPSIS suitability surfaces |
| `data/raw/list/` | LIST vector data: TASVEG 5.0, hydrographic lines and areas, transport segments |
| `data/raw/points/` | Start/end access points and summits (created in ArcGIS Pro) |
| `data/processed/` | 10 m DEM, slope, the constraint mask (`constraints.tif`) and the WLC and TOPSIS suitability rasters |
| `data/processed/criteria/` | The five standardised criteria rasters (slope, vegetation, streams, wetland, access) |
| `environment.yml` | Conda environment for running the scripts and notebooks |
| `*.png` | Figures used in the Jupyter Book |
| `MCDA.ipynb`, `walking_cost.ipynb`, `track_roadprocessing.ipynb`, `TASVEGprocessing.ipynb` | Working notebooks |

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


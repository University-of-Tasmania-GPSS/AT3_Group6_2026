# Introduction

KGG375 GIS Project (AT3), University of Tasmania, 2026

## Motivation
Tasmania is filled with beautiful scenery and untouched wilderness. This includes the Cheyne Range, located in the Central Highlands, it includes some of Tasmania's highest peaks, and is contained within the Franklin - Gordon Wild Rivers National Park, which are part the Tasmanian Wilderness World Heritage Area. This is a well known walking location but is currently entirely off-track making it only for experienced bush-walkers.

```{image} Cheyne Range.jpg
:alt: Walkers on the Cheyne Range
```

*Walkers on the Cheyne Range. Photo: © Louise Fairfax.*

## Background
Off-track walking in places like the Cheyne Range creates informal trails called "pads". These tend to widen and erode over time especially on fragile alpine vegetation (Whinam & Chilcott, 2003; Dixon et al., 2004). the Chenye range is home to many threatened vegetation features such as populations of pencil pines (Athrotaxis cupressoides) King Billy (Athrotaxis selaginoides) and Nothofagus gunni alongside blanket bogs that form a recognised conservation value in the Tasmanian Wilderness World Heritage Area (TWWHA), these are composed primarily of Buttongrass moorland alongside sphagnum bogs. This area is also the site of a glacial valley of geo-conservation signifgence which forms part of the Tasmanian Geoconservation Database.

A planned hardened track can protect the surrounding landscape, this can be implemented through installing raised track features or avoiding vegetation and soil types prone to degrading. Deciding where to put this track requires the weighing of many environmental factors at once such as slope and vegetation type. MCDA is currently the standard way to combine environmental factors into a suitability map in which we will be using WLC and TOPSIS. To weight the criteria we used AHP.

```{image} buttongrass_and_mud.jpeg
:alt: Walkers knee deep in mud surrounded by button-grass
```

*Walkers Knee deep in mud, in a button grass moorland. Photo: © Steve Vertigan.*

## Objectives
The aim of this project is to model and compare optimal trails that go through the Cheyne range which weighs key environmental factors, and walking cost to find the optimal route for multiple start locations.

Objectives:
1. Develop and compare two suitability models for a walking track using different decision rules (WLC and TOPSIS)
2. Implement a movement cost model that accounts for the effort of uphill and downhill walking.
3. Generate and compare routes from different start points using a least-cost path algorithm.
4. Compare and visualise the resulting routes using maps and elevation profiles.


## Cheyne Range Visualisation
:::{iframe} https://university-of-tasmania-gpss.github.io/AT3_Group6_2026/dem_3d.html
:width: 100%
:height: 600px
:::

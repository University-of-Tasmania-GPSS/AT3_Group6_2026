# Discussion

## Main hurdles and problems

The main hurdle on the criteria and suitability side of the project was deciding what to use and how it should be weighted. This came from looking to past research and finding threatened vegetation and past modelling / pathfinding literature.

another key hurdle was data processing, pathfinding algorithms are computationally intensive, one way this was managed was to reduce the DEM from a 1m dem to a 10m dem, this should still be appropriate for a walking trail, particularly one covering over 10km. 

## Alternative approaches
Alternative approaches include using different criteria and constraints. We chose the ones that we thought to be most important and that were backed up by literature. It can be made more comprehensive if we added more criteria into the suitability.

Another approach could also be to use a different weighting method. In this project we chose to use AHP as it allows the criteria to be ranked against each other and then the weights are pulled from that. The issue with this is that it is still subjective and requires the criteria to be ranked appropriately.

The way the suitability score is calculated can also be changed. In this project we chose to make two rasters using WLC and TOPSIS. This was because these two methods are what we are familiar with. A different method to producing a suitability raster could be used which would handle the weights differently and produce an alternative raster.

Another factor that we did not explore fully is combining different routes to force the trail to go to different peaks. This was explored and we made the code for it but decided that it was beyond the scope of the current project. By combining routes it could potentially create multiday trails through the range for epic days out. We decided that we would not have the time to complete comparisons between these routes as it would be handling a lot more data and more judgement calls. This would also create the possiblity for a circut style trail rather then a out and back or through hike.

We also only used one method of path optimisation which was Dijkstra. Another method we could have used would have been A*. By utilising another path optimisation method we could have made further comparisons on the routes. 

## Limitations

Some limitations of the project start at the data we used. The DEM we used was resampled to the 10 metre level so that processing routes would become more efficient. The downside to doing this is that the slope and routes can be incorrect at a more detailed scale. This could be solved by using the 1 metre or 2 metre DEM.

The TASVEG data set is mapped at a large scale as well, so small patches of vegetation can be missed or misplaced. Our constraints are assuming that this dataset is the truth and avoiding where it says the threatened veg is. This would have to be field checked to ensure that what we are assuming to be true actually is.

The hydrography data set also misses small features such as seasonal streams. These are not incorporated into the model and routes may traverse through here. A method to avoid this would be to create a model of water streams that would map where seasonal water is likely to be and then get the hydrography lines from this dataset.

The weights in the AHP table are subjective and based on our judgement. Thus, the suitability raster is also entirely based on how we judged the weights. 

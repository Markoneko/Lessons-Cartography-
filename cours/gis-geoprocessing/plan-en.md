# Plan — GIS: Geoprocessing

> Fichier généré à chaque compilation à partir des fiches de `index-en.qmd`.
> Ne pas le modifier : pour changer le plan, modifier les fiches.

| N° | Diapo | Niveau | État | Intention | Expérience | Demande |
|----|-------|--------|------|-----------|------------|---------|
| 0.1 | Couverture |  | à revoir | Cover. Presented before the practical, then read on one’s own. [PPT 1] | none |  |
| 0.2 | How to use this handout |  | à revoir | The same user guide as “GIS: Basics” (levels, exercises, bonuses), without the revision system, not ready yet. Prerequisites: raster, vector, attributes and layers, from “GIS: Basics”. [new] | none |  |
| 0.3 | What you will be able to do |  | à revoir | Three verbs, three parts: query a layer, enrich its attributes, create new features; then the same moves in raster, and going from one to the other. [PPT 2] | none |  |
| 0.4 | Course map |  | à revoir | The five parts and the key to the three levels. | links to each slide |  |
| 1.0 | Querying | partie | à revoir | Selecting the features that meet criteria. [PPT 3] | none |  |
| 1.1 | A question put to the database | Core | à revoir | An attribute or spatial query is a question put to the database to display, sort, edit or analyse. SQL, the standard language of relational databases, based on relational algebra. [PPT 3] | sort four forest questions into “attribute” or “spatial” |  |
| 1.2 | SELECT, FROM, WHERE | Core | à revoir | The basic form of a query: the fields wanted, the layer, the conditions. The ArcGIS screenshot is replaced by the written query, with its QGIS equivalent (select by expression). [PPT 4] | put a query on the stands in order (SELECT, FROM, WHERE, condition) |  |
| 1.3 | Comparing | Core | à revoir | Comparison operators: =, <>, <, >, <=, >=; attribute queries only. [PPT 5] | multiple choice: which condition keeps the stands that are not oak? |  |
| 1.4 | Calculating | Support | à revoir | Mathematical operations (sum, product, power, trigonometry) and statistics (sum, mean, extremes, standard deviation) in a query. Forest example: a stem density per hectare. [PPT 6] | question: how do you compute the stem density of a stand from two fields? |  |
| 1.5 | Querying space | Core | à revoir | Topological and distance operators, which make a spatial query: intersects, contains, within a distance of… The svgopen.org screenshots are redrawn as one diagram. [PPT 7] | diagram of the three relationships; multiple choice: which operator for “the stands crossed by a forest road”? |  |
| 1.6 | Combining criteria | Core | à revoir | Boolean operators AND, OR, NOT, between two or more criteria, read on Venn diagrams. [PPT 8] | multiple choice with diagram: oak AND over 5 ha, or oak OR over 5 ha? |  |
| 2.0 | Enriching attributes | partie | à revoir | Adding to the table what the geometry already knows. [PPT 9] | none |  |
| 2.1 | Measuring | Support | à revoir | The metric properties of features (centroid, length, perimeter, area) become fields. Distance between features: Cartesian on the plane, great-circle on the sphere; see “From the Earth to the Map”. [PPT 9] | question: why is the Paris – New York distance not the same on a Mercator map and on the globe? |  |
| 2.2 | The spatial join | Core | à revoir | Joining two layers by position rather than by a key: each feature receives the attributes of the feature that contains it. Forest example: each inventory plot receives the species of the stand it falls in. Diagram redrawn. [PPT 10] | question (prediction): which table do you get after the join? With the answer, the new column appears to the right of the table, with an arrow from the stands. |  |
| 3.0 | Creating features | partie | à revoir | New geometries, computed from the old ones. [PPT 12] | none |  |
| 3.1 | Changing the geometry type | Support | à revoir | From points to a line (a path), from points to a polygon (the convex hull), from a polygon to a point (the centroid). [PPT 12] | sort: which tool to go from the GPS readings of a road to its line? from the trees of a plot to its footprint? from a stand to its label? |  |
| 3.2 | Buffers | Core | à revoir | An area of influence at a fixed distance around a feature; dissolved or separate buffers; multiple buffers. Forest example: the 50 m strip along forest roads, or around rivers. Diagram redrawn. [PPT 13] | question (prediction): three overlapping buffers, dissolved or not: how many features come out? |  |
| 3.3 | Overlaying: clip, union, intersect | Core | à revoir | Geoprocessing based on overlay: clip, union, intersection. What changes: the geometry kept, and the attributes inherited. Diagram redrawn. [PPT 14] | sort three forest needs into their tool (keep only the municipality; the whole area of both layers; only the common part with the attributes of both) |  |
| 3.4 | Dissolving on an attribute | Core | à revoir | Dissolve groups the features that share the same value: six parcels, three zones. Forest example: from parcels to management series. [PPT 15] | question (prediction): how many features remain after dissolving on the “zone” field? |  |
| 3.5 | Going further: spatial analysis | Further | à revoir | More specialised tools, borrowed from spatial analysis: point pattern analysis, spatial autocorrelation, interpolation, optimal location, shortest path. [PPT 16] | none |  |
| 4.0 | Raster processing | partie | à revoir | The same questions, asked of a grid: a summary. [PPT 17] | none |  |
| 4.1 | Three families of operations | Support | à revoir | Local (cell by cell), focal (from neighbouring cells), zonal (by zone). Three small grid diagrams, instead of Jeremy Mennis’s figures. [PPT 18, 19, 30, 38] | diagram; sort five forest tasks into their family |  |
| 4.2 | Local: reclassify, apply a condition | Support | à revoir | Reclassify (a lookup table, or n automatic classes); apply a condition, often a threshold. Uses: a binary mask, a simplified classification. Forest example: slopes over 30%, too steep for machines. Small grid diagram. [PPT 20, 21, 29] | question: on a slope grid, which cells equal 1 after the condition “slope > 30”? |  |
| 4.3 | Local: calculating across layers | Support | à revoir | Raster algebra (the raster calculator): a layer and a constant, or several layers cell by cell (sum, mean). Example: the NDVI, a vegetation index. Weighted overlay, for a composite index. Small diagrams. [PPT 22 to 27] | none; bonus: weighted overlay. The 0.3 threshold between vegetation and no vegetation is given. |  |
| 4.4 | Layers that do not line up | Support | à revoir | The raster calculator is powerful, but two grids with different resolution or alignment do not overlay cell by cell: they must first be made consistent. [PPT 28] | diagram of two offset grids |  |
| 4.5 | Focal: the moving window | Support | à revoir | Each cell receives a value computed from its neighbours, in a 3 × 3, 5 × 5… window; the shape of the neighbourhood can vary. Filters and focal statistics. Small diagram. [PPT 31, 32, 33] | question: what value does the centre cell receive with a 3 × 3 mean? |  |
| 4.6 | Focal: deriving the terrain | Support | à revoir | From the DTM come slope, aspect, hillshade. DTM (the ground) and DSM (ground and above-ground); their difference gives vegetation height: the link with the forest. [PPT 34, 35, 36] | diagram DSM − DTM = canopy height; question: where can you read tree height? |  |
| 4.7 | Focal: distance | Support | à revoir | Euclidean distance: each cell receives its distance to the nearest source; with a maximum, you get a raster buffer. [PPT 37] | none |  |
| 4.8 | Zonal | Support | à revoir | A statistic computed over the cells of the same zone (mean, sum, maximum…), the zones being given by a raster or a vector. Small diagram. [PPT 38, 39] | question: what is the mean of zone B? |  |
| 4.9 | Other common operations | Support | à revoir | Resample (change the resolution), clip, extract; then more complex processing: interpolation, watersheds, solar radiation, visibility. [PPT 40, 42] | none |  |
| 5.0 | Between raster and vector | partie | à revoir | Processing that straddles the two modes, the kind most used in forestry. [new] | none |  |
| 5.1 | Rasterise, vectorise | Core | à revoir | From vector to raster: each cell takes the value of the feature that covers it. From raster to vector: neighbouring cells with the same value become a polygon; example: from a classified image to a land cover map. What is lost each way. [PPT 11, 41] | compare: slider between the vector parcels and their rasterised version |  |
| 5.2 | The zoning changes the result | Further | à revoir | The modifiable areal unit problem (MAUP): the same data, aggregated with two different zonings, give two different maps. The two European maps from the old handout. [PPT 11] | scroll through the two maps; question: why do they not tell the same story? |  |
| 5.3 | Summarising a raster by polygons | Core | à revoir | Zonal statistics with vector zones: the mean slope of each parcel, the mean height of each stand. The result goes back into the attribute table. [PPT 39] | question (prediction): which field is added to the parcel table? |  |
| 5.4 | Clipping a raster by a vector | Support | à revoir | The mask: keep only the DTM cells inside the forest. [PPT 40] | none |  |
| 5.5 | Reading a raster under points | Support | à revoir | Sampling: each point receives the value of the cell under it; example: the elevation or slope of each inventory plot. [PPT 40] | question: what value does plot 3 receive? |  |
| 5.6 | Draping and extruding | Further | à revoir | Draping an image over the DTM, extruding vector features by an attribute: the 3D view, where raster and vector meet. [PPT 43, 44] | scroll through the two images |  |
| 6.1 | Key points |  | à revoir | The core slides, in one list. | links to each slide |  |
| 6.2 | Your turn |  | à revoir | Points to the geoprocessing practical: the investigation on forest data. | none |  |
| 6.3 | Sources and credits |  | à revoir | Sources of the figures reused (ESRI, FAO, ESPON, etc.), to be completed. [new] | none |  |

## Où en est-on

- 40 diapos, dont 0 figées, 40 à revoir, 0 à réaliser.
- Aucune demande en attente.

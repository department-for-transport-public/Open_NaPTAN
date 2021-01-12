# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

===============
### File Export 

- Capability to produce a template file for submitting new stations

### Second set of initial checks

#### Data pipeline

- NPTG datafeed from live server.
- Download only the area that is requested, mapping the areas to their id numbers
- add logging information for process run.
- remove all the unnecessary data after running the checks, clean up function.

#### Geospatial Checks

- Polygon based checks, need accurate polygon representation of areas/localitys/stop groups
- Hail and ride section length
- Locality with geocode Outside - the folium algorithm for sorting groups together into polygons. I think accounts for this, as other checks ensure that stops are in the correct locality, using geocode for this has many issues.
- So this could be checked by making sure the length / shape is sensible
- Stops in parent locality
- Localities contained by non-parent (90% rule)
- Localities overlapped (40-89% rule)
- Locality with Unusual shape elongated shape
- Stops with wrong types
- Unused Locality Near Stops
- Stop proximity
- Needs road map network api
- Machine Learning based or NLP.
- Stops with wrong bearing, need to understand local geography and road layout
- Stop area Members with different localities
- Hail and ride invalid - the hail and ride file is empty and has been for some time, this check is impossible then. A similar thing could be done.
- Stop road distance
- Need a road network dataset to know where the roads, are then find all the nearest roads to Naptan points…
- Coast line checks, refine check to pinpoint to within 20 ms of coastline
graduanity.

### Internal Consistency Checks

- Stop area members without identical names
- Stops in Different authorities
- Stops in alternate localities
- Locality Not unique
- Stop names with repeating words
- check that atcocodes are the correct format.
- check naptan localities are consistent with nptg dataset.
- checks if a column has any nan or null values.

### Visualisation

- displaying stop areas and localities.
- Add relevant issues and relevant errors
- Checking localities polygons overlap
- Display critical warning on interactive maps
- change between showing all stops and critical stop warnings (only high warnings.)

### Report

- consistent report function for when area passes given test.

## [0.0.3] - 2020-11-04

### Added

- Now downloads the publicly available nptg dataset for data cleansing checks.
- change between showing all stops and critical stop warnings (only high warnings.)
- added setup.py file
- travis yaml (12/08/2020)
- check atcocode length is not less than 12 alphanumeric characters.(12/10/2020)
- Check the creation and mod dates are not after today's date or before.
- filter_bus_stops to improve performance of bus stop checks.
- checks if a column has any nan or null values.
- check name length is correct,
- Naptan structure checks for extreme changes with the data when it is download.

### Changed

- renaming of existing checks, using more OOP structures, associated checks with
classes
- how reports are generated and the details contained within has changed
- checks now have warning levels, (low, medium, high, na), to indicated severity
- checks now have geographical impact levels, (stops, stop area, locality, admin areas, regions)
- filter bus stop methods.
- add check soft 'interface' class
- no removing of illegal chars and capitals, just reporting.
- uses pylance for environmental management, more stable than existing python language server.
-- removed check init files
- added explicit epsg:4326.
- stops clusters replaced with base map (60% speed improvement), better 
- add sq area and miles display to measurement calculation tool.

### Fixed

- fix crs future warning epsg incompatibility.
- fixed illegal chars check (07/10/2020)
- fixed map messages (24/08/2020)
- polygon admin area display fixed with 0.2 buffer for concave hull calculations.
- stop_name_contains_locality_name

### Removed

## [0.0.2] - 2020-08-26

-----------------------;

### Added

- Kent Interactive html example map

## [0.0.1] - 2020-07-02

-----------------------;

### Added

- The first release of Open NaPTAN
- etl of naptan data from naptan web service.
- Download Naptan Data
- Extract Naptan files
- Check Naptan Files are correct
- Convert to lat lon
- deactivated nodes
- Calculate_Naptan_Geometry
- Get_Centroid_Of_Naptan_Area
- read naptan files into dataframe
- Non-standard stop area generation
- Create_Locality_From_Column
- Loads naptan gazette data
- Map gazette data to node data
- intersect list to dataframe mask.

#### Data Cleansing Methods

- Strip illegal characters
- Basic warning information outputted
- Reporting of naptan node error.

#### Consistency checks

- Stop_With_Multiple_Road_Names
- Remove_Illegal_Spaces
- Remove_Illegal_Characters
- Stop_With_Bearing_Missing
- Stop_Name_Contains_Locality_Name
- Check_Name_Too_Long
- Stop_Names_With_High_Risk_Words
- Identify_Illegal_Captials
- Localities_with_Identical_Stops

#### Geospatial Checks

- Get_Nearest_Road_Name
- Calculate_Nearest
- Nearest_Naptan_Stop
- Node_Distances
- Naptan_Coastal_Nodes
- Check_Polygon_Intersections
- Road_Name_Matches_Coordinates

#### Visualisation

- Admin areas

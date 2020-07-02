# %%
import sys
import timeit
from datetime import datetime
from pathlib import Path

# Visualisations Libraries
import folium
import geopandas as gpd
import numpy as np
import pandas as pd 
import geojson

from geopy import distance
from geopy.geocoders import Nominatim
from shapely.geometry import Point

from shapely.ops import nearest_points
from global_land_mask import globe

# homebrew
import etl_pipeline as etl
import reporting as report
import visualiser as vis


# %%
# config options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 12)
pd.options.mode.chained_assignment = None
timestr = datetime.now().strftime("%Y_%m_%d")


# %%
def check_polygons_intersect(gdf):
    """[summary] provide a gdf or shapefile, will return the polygons that
    intersect within the given gdf which has a list of polygons.

    Arguments:
        gdf {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    # df = gp.read_file(file) # open file
    # df["NEIGHBORS"] = None  # add NEIGHBORS column
    list(gdf)
    name = gdf.head(1)

    for index, LocalityName_Locality in gdf.iterrows():
        # get 'not disjoint' countries
        neighbors = gdf[~gdf.geometry.disjoint(LocalityName_Locality.geometry)].tolist()
        # remove own name from the list
        neighbors = [name for name in neighbors if LocalityName_Locality != name]
        # add names of neighbors as NEIGHBORS value
        gdf.at[index, "neighbouring_lads"] = ", ".join(neighbors)

    # save GeoDataFrame as a new file
    # gdf.to_file(f"{os.getcwd()}/polygons/{name}.shp")
    return gdf


# %%
def check_polygon_lengths(polygon):
    """[summary] Get the longest side of a given polygon, in meters

    Arguments:
        polygon {[shapely.geometry.polygon.Polygon]} -- [the polygon of the 
        given area, ]

    Raises:
        NotImplemented: [description]

    Returns:
        [type] -- [description]
    """
    # get minimum bounding box around polygon
    box = polygon.minimum_rotated_rectangle
    # get coordinates of polygon vertices
    x, y = box.exterior.coords.xy
    # get length of bounding box longest edge
    edge_length = distance(Point(x[0], y[0]).distance(Point(x[1], y[1])),
                           Point(x[1], y[1]).distance(Point(x[2], y[2]))).meters
    return edge_length
    raise NotImplementedError


# %%
def polygon_length_is_regular(df_area, polygon):
    """[summary] when given a geodataframe, checks the matching polygon, is
    under a 1000

    Args:
        df ([naptan geodataframe]): [description]
        polygon ([[shapely.geometry.polygon.Polygon]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    poly_length = check_polygon_lengths(polygon)
    if poly_length <= 1000:
        print('Polygon area is regular')
    else:
        df_area
    return failed_nodes
    raise NotImplementedError


# %%
def check_naptan_area_shape(gdf):
    """[summary] given a gdf dataframe that is not larger than a locality,
     if it is then we raise an error. Assuming the area is correct, we then
    generate an alphashape concave polygon and check the length of the longest
    side, if the longest side is too long, then we know there is an issue with
    the area shape.

    Args:
        gdf ([geodataframe]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    # we check to make sure the given dataframe is not larger than locality.
    if len(f'{gdf}') > 500:
        print('The given area is too large to check.')
        raise NotImplementedError
    else:
        polygon = vis.create_concave_polygon(gdf)
        report = polygon_length_is_regular(gdf, polygon)
    return report
    raise NotImplementedError


# %%
def get_nearest_road_name(gdf, ATCOCode):
    """[summary] -> Goes out to Nomatnium to get nearest road name,
    to set of coordinates. Must have an atcocode column. Atcocode must be in
    the provided dataframe.

    Arguments:
        gdf {[geopandas dataframe]}-- [Naptan dataframe we are searching within
        can be a locality, an area or a stop area.]
        ATCOCode {[str]} -- [look up code we are checking. Vectorise for list.]

    Returns:
        [roadname] -- [returns road name of a set of coordinates.]
    """
    try:
        node = gdf[gdf['ATCOCode'].str.contains(ATCOCode,
                                                regex=False)]
        lat = node.Latitude.iloc[0]
        lon = node.Longitude.iloc[0]
        geolocator = Nominatim()
        location = geolocator.reverse(lat, lon)
        road_name = ('Road name is: ',
                     location.raw.get('address', {})
                     .get('road'))
        return road_name
    except (IndexError) as e:
        log.critical(f'{e}, Value not found in given dataframe.')
    except (ValueError) as e:
        log.debug(e)


# %%
def calculate_nearest(row, destination, val, col="geometry"):
    """[summary] use shapely unary_union and nearest point to a given point
    stored in the supplied dataframe.

    Arguments:
        row {[type]} -- [the data frame row]
        destination {[type]} -- [a dataframe obj with destination coordinates
        for comparing against.]
        val {[type]} -- [the field value to match against, using as a numpy
         array]

    Keyword Arguments:
        col {str} -- [description] (default: {"geometry"})

    Returns:
        [type] -- [description]
    """
    dest_unary = destination["geometry"].unary_union
    nearest_geom = nearest_points(row[col], dest_unary)
    match_geom = destination.loc[destination.geometry == nearest_geom[1]]
    match_value = match_geom[val].to_numpy()[0]
    return match_value


# %%
def nearest_naptan_stop(filename, locality, atcocode, geo="geometry"):
    """[summary] Returns the next nearest node in the Naptan network to a given
    stop in the same locality.

    Arguments:
        FileName {[type]} -- [Is a file name string of naptan sub dataset]
        Locality {[type]} -- [A named locality, only the given names in the
        Atcocode file will work.]
        StopCode {[type]} -- [the atcocode for the given node to find the
        nearest neighbour in the same locality.] 

    Keyword Arguments:
        geo {str} -- [description] (default: {"geometry"})

    Returns:
        [type] -- [description]
    """
    # TODO add multidirectional bearing filtering for finding the nearest stop
    # in any cartianal direction.
    # TODO add error handling for if a given node is outside the stated locality
    # TODO get the bearing of where the stop is???

    df_auth = etl.Create_Naptan_Geometry_File(filename)
    df_local = etl.Create_Locality_Frame(df_auth, locality)
    local_gdf = etl.Create_GeoDataFrame(df_local)
    parent_Lat, parent_Long = etl.get_centroid_naptan_area(local_gdf)
    node = local_gdf.loc[local_gdf['ATCOCode'] == atcocode]
    local_gdf = local_gdf[local_gdf.ATCOCode != node.ATCOCode.values[0]]
    node['nearest_geom'] = node.apply(calculate_nearest,
                                      destination=local_gdf,
                                      val=geo,
                                      axis=1)
    node['nearest_node'] = node.apply(calculate_nearest,
                                      destination=local_gdf,
                                      val='ATCOCode',
                                      axis=1)
    nearest_node = local_gdf.loc[local_gdf['ATCOCode'] == node.nearest_node.values[0]]
    local_points = zip(local_gdf.Latitude, local_gdf.Longitude)
    m = folium.Map(location=[parent_Lat, parent_Long], zoom_start=12)
    for location in local_points:
        folium.CircleMarker(location=location,
                            color='white',
                            radius=2).add_to(m)
    folium.Marker(location=[nearest_node.Latitude, nearest_node.Longitude],
                  popup=nearest_node.ATCOCode).add_to(m)
    folium.Marker(location=[node.Latitude, node.Longitude],
                  popup=node.ATCOCode).add_to(m)
    return nearest_node, m


# %%
def node_distance(node1, node2, min_distance, max_distance):
    """[summary] Calulcates whether a naptan node distance in meters, using
    geodesic formulate

    Arguments:
        node1 {[type]} -- [description]
        node2 {[type]} -- [description]
        min_distance -- the min distance in meters that should be between two
        nodes.
        max_dist {[float]} -- the max distance in meters that can be between
        the nodes

    Returns:
        Distance [str] -- [description]
    """

    lat_n1, lon_n1 = node1.Latitude, node1.Longitude
    lat_n2, lon_n2 = node2.Latitude, node2.Longitude
    distance = distance((lat_n1.values[0], lon_n1.values[0]),
                        (lat_n2.values[0], lon_n2.values[0])).meters

    if (distance >= max_distance):
        return ('Nodes are too far away.')
    if (distance <= min_distance):
        return ('Nodes are too close.')
    else:
        return (f'Stop is within; {distance:.2f} meters.')


# %%
def naptan_coastal_nodes(gdf):
    # TODO - add a column to the master naptan dataframe, and then count up
    #  false values, to get the percent of stops that fail, and then compare
    #  those stops, to find out which ones are near the coast and how near
    #  the coast they are.
    """[summary] provided a dataframe, returns a list of nodes that are near the
    coast line, this uses global land mask library, a numpy & pandas extension, 
    for mapping the boundaries of the coastline.

    Arguments:
        df {[geospatial dataframe]} -- [the naptan master dataframe.]

    Raises:
        ve: [Raises description]
        e:  []
    Returns:
        [type] -- [description]
    """

    check_name = naptan_coastal_nodes.__name__
    try:
        gdf['Land_State'] = globe.is_land(gdf['Latitude'],
                                          gdf['Longitude'])
        coastal_nodes = gdf.loc[~gdf.Land_State]
        high_node_areas = coastal_nodes['LocalityName'].value_counts()
        percentage = ((len(coastal_nodes) / len(gdf)) * 100.0)
        if percentage >= 1.1:
            print(f"The area has a total of {coastal_nodes}, nodes which are \
                    at sea error ratio is {percentage:0.2f}% too high.")
        elif percentage <= 0:
            print('No Nodes were found along the coastline')
            pass
        else:
            print(f"The area has a total of {coastal_nodes} in the area.\
                  {percentage:0.2f}")
        report.nodes_error_reporting(gdf, check_name, coastal_nodes)
        return high_node_areas

    except ValueError as ve:
        raise(ve)

    except Exception as e:
        print(e)


# %%
def road_name_matches_coordinates(gdf, ATCOCode):
    """[summary] Checks that the road name in the record, matches if the 
       The “street” shown in the data does not correspond with the name attached
       to the road segment to which the stop is snapped in the Navteq mapping
       data used by Ito.
    Arguments:
        gdf {[geopandas dataframe]} -- [pass in the chosen dataframe]
        ATCOCode {[str]} -- [Pass in the given naptan unique stop id.]

    Returns:
        [type] -- [description]
    """
    check_name = road_name_matches_coordinates.__name__
    gdf1 = gdf
    node = gdf1.loc[gdf1['ATCOCode'] == ATCOCode]
    found_name = get_nearest_road_name(gdf1, ATCOCode)
    if found_name[1] == node['Street'][0]:
        print('Road Name Matches')
        pass
    else:
        res = node["ATCOCode"]
        report.nodes_error_reporting(gdf, check_name, res)
    return res


# %%
def stops_with_wrong_bearing(gdf):
    """ Descriptions: The bearing shown in the data does not correspond with
        the bearing as calculated by reference to the orientation of the road
        at the location of the stopping point.

        Args:

        Returns:
    """
    pass


# %%
def stop_proximity(gdf):
    """ Descriptions: Stop is too close to another stop, any stop within 4 meters of another stop will flag as a warning. BCS type the threshold is 2 meters

        Args:

        Returns:
    """
    pass


# %%
def stops_in_different_admin_authority_geo_position(gdf, stops, authorities):
    """[summary] The AtcoCode prefix for the StopPoint represents an
    AdminArea other than the one associated with the stop‟s Locality.
    This test highlights those stops which are associated with a locality that
    is itself not in the same administrative area. This is often not wrong – 
    but in some cases it indicates a stop that is incorrectly located, or 
    associated with the wrong locality.

    Check each example and confirm that each represents a stop close to the
    boundary of your authority‟s area – and consider whether the locality
    association with each stop is reasonable, even if it is with a locality
    that is in the adjacent admin area. Check that the coordinates of the stop
    are right, and correct them if not. 
    Args:
        gdf ([gdf]): [the naptan total dataframe]
        stops ([node_type_stops]): [description]
        authorities ([gdf]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = stops_in_different_admin_authority_geo_position.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def unused_locality_near_stops(gdf):
    """[summary]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = unused_locality_near_stops.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def stop_area_members_with_different_localities(gdf):
    """[summary]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = stop_area_members_with_different_localities.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def stop_with_wrong_types(gdf):
    """[summary]

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = stop_with_wrong_types.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def stop_with_wrong_types(gdf):
    """[summary]

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = stop_with_wrong_types.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def hail_ride_invalid(gdf):
    """[summary]

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = hail_ride_invalid.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def stop_road_distance(gdf):
    """[summary]

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = stop_road_distance.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def locality_with_geocode_outside(gdf):
    """[summary]

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = locality_with_geocode_outside.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def stops_in_parent_locality(gdf):
    """[summary]

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = stops_in_parent_locality.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def localities_contained_by_non_parent(gdf):
    """[summary] 

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    #TODO use for both 90% overlap rule and 40-89% rule.
    check_name = localities_contained_by_non_parent.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def hail_ride_section_length(gdf):
    """[summary] 

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = hail_ride_section_length.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def locality_with_unusually_elongated_shape(gdf):
    """[summary] 

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = hail_ride_section_length.__name__
    # list of stops not in correct admin areas by geo position.
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError

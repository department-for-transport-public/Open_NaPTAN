# %%
from etl import etl_pipe
import alphashape
from geopy.geocoders import Nominatim
from shapely.ops import nearest_points
from shapely.geometry import Polygon, LineString, Point
from shapely.geometry import shape
from geopy import distance

import folium
from convertbng.util import convert_lonlat
from datetime import datetime
from pathlib import Path
import sys
# for performance fun times.


# libraries
import pandas as pd
import numpy as np
import geopandas as gpd
# network mapping.
import matplotlib.cm as cm
import matplotlib.colors as colors


# %%
# config options
timestr = datetime.now().strftime("%Y_%m_%d")
dl_home = Path(Path.home() / 'Downloads')
node_dir = Path(f'{dl_home}/Naptan_Data/{timestr}_naptan_nodes/')
nptg_dir = Path(f'{dl_home}/Naptan_Data/{timestr}_nptg/')
geojson_dir = Path(f"{dl_home}/Naptan_Geojson/{timestr}_geojson/")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 5)
# declare geo coordinates conversion type.
crs = "EPSG:4326"


# %%
def make_naptan_polygon(gdf):
    """[summary] calcuates using shapely functions, to buffer

    Args:
        gdf ([type]): [description]
    """
    # cast polygon to a shapely geometry
    polygon_geom = Polygon(zip(gdf['Longitude'],
                               gdf['Latitude']))
    # we use convex hull rather than concave hull as this is more
    #  representative of reality.
    polygon_geom2 = polygon_geom.convex_hull
    # add a buffer layer to the polygon, this will show overlapping areas.
    naptan_polygon = polygon_geom2.buffer(0.001)
    """
    # use cascaded union to determine the boundary, but this is computational
    expense, like impractically so.
    naptan_polygon = cascaded_union(polygon_geom2)
    """
    return naptan_polygon

# %%


def convert_to_lat_long(df):
    """Descriptions: Converts 100,000+ coordinates in a dataframe
     into accurate longitude and latitude adding the columns where they are
     missing from a dataframe.

    Arguments:
        df {[type]} -- [description]
        file_name {[type]} -- [description]
    """
    easting_np = np.array(df.Easting)
    northing_np = np.array(df.Northing)
    res_list_np = convert_lonlat(easting_np, northing_np)
    df['Longitude'], df['Latitude'] = res_list_np[0], res_list_np[1]
    # drop the easting and northing columns, now we are done with them.
    df = df.drop(columns=['Easting', 'Northing'], axis=1)
    return df


# %%
def calculate_naptan_geometry(gdf):
    """[summary] Takes in a pandas dataframe and returns a geodataframe
    with a geometry column calculate from using lat and lon CRS.

    Args:
        df ([pandas dataframe]): [description]

    Returns:
        [geodataframe]: [description]
    """
    try:
        # Coordinate reference system : WGS84
        # direct crs assignment as specified in geopandas 0.7
        # https://geopandas.readthedocs.io/en/latest/projections.html#upgrading-to-geopandas-0-7-with-pyproj-2-2-and-proj-6
        gdf = gpd.GeoDataFrame(gdf,
                               geometry=gpd.points_from_xy(gdf.Longitude,
                                                           gdf.Latitude))
        # recast the dataframe.
        gdf = gpd.GeoDataFrame(gdf,
                               crs="EPSG:4326")
        # check there are no empty values
        if not gdf.is_empty.any():
            # check the geometry is valid.
            if gdf.is_valid.all():
                return gdf

    except ValueError as ve:
        sys.exit(f"Naptan geometry couldn't be calculated because of {ve}.")

    except Exception as e:
        sys.exit(f"Naptan geometry conversion failed {e}.")


# %%
@ NotImplementedError
def create_naptan_multi_polygon(gdf):
    """[summary] creates a multipolygon when given a naptan geodataframe.

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]
        e: [description]
        ve: [description]
        OSError: [description]
        file_missing: [description]
        NotImplementedError: [description]
        NotImplementedError: [description]
        ve: [description]

    Returns:
        [type]: [description]
    """
    raise NotImplementedError

# %%


def fetch_osm_region_data(region_name):
    """[summary] returns a data feed of osm region data for the given localtiy

    Args:
        region_name ([type]): [Naptan Locality data]
    """
    # set tags of relevant types of data
    tags = {'amenity': True,
            'landuse': ['retail', 'commercial'],
            'highway': 'bus_stop'}
    # fetch the data
    gg = ox.pois_from_place(f'{region_name}, United Kingdom', tags)
    # remove unused fields
    gg = gg[['osmid', 'geometry', 'amenity', 'operator', 'name', 'highway']]
    #
    gg = gg[gg['highway'] == 'bus_stop'].dropna(axis=1, how='any').head(4)
    #
    m = folium.Map(location=[gg.geometry.x, gg.geometry.y])
    return m


"""
example = 'Guildford, Surrey'
fetch_osm_region_data(example)
"""


# %%
def find_nearest_neighbour(gdf):
    """[summary] provide a gdf or shapefile, will return the polygons that
    intersect within the given gdf which has a list of polygons.

    Arguments:
        gdf {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    # list(gdf)
    name = gdf.head(1)

    for index, locality_name in gdf.iterrows():
        # get 'not disjoint' countries
        neighbors = gdf[~gdf.geometry.disjoint(
            locality_name.geometry)].tolist()
        # remove own name from the list
        neighbors = [name for name in neighbors if locality_name != name]
        # add names of neighbors as NEIGHBORS value
        gdf.at[index, "neighbouring_lads"] = ", ".join(neighbors)
    return gdf


# %%
@ NotImplementedError
def map_naptan_neighbours(gdf, naptan_column='LocalityName'):
    """[summary] finds the naptan localities/areas that are nearest any other
    given naptan area.

    Args:
        gdf ([type]): [description]
        naptan_column (str, optional): [description]. Defaults to 'LocalityName'.
    """
    pass


# %%
def coord_lister(geom):
    """[summary] when given a geometry pandas geoseries, returns an exterior
    list of coordinates for all of the entries, given should

    Args:
        geom ([type]): [description]

    Returns:
        [type]: [description]
    """
    coords = list(geom.exterior.coords)
    return (coords)


# %%
def save_polygon_data_format(naptan_polygon,
                             area_name,
                             naptan_column):
    """[summary] saves naptan polygon data, into a variety of formats for later
    usage by other analytical tools.

    Args:
        naptan_polygon ([type]): [description]
        area_name ([type]): [description]
        naptan_column ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Declare the result as a new a GeoDataFrame
    naptan_polygon = gpd.GeoDataFrame(naptan_polygon,
                                      crs="EPSG:4326",
                                      geometry='geometry')
    # save the result as a geopackage file, the given replacement to
    #  shp file, should work
    # area_name = file_label_aggregation(gdf)
    naptan_polygon.to_file(f"{dl_home}/{area_name}_.gpkg",
                           layer=f'{naptan_column}',
                           driver="GPKG")
    # saves the result as a geojson file.
    # TODO, check if this replaces the naptan geojson function.
    naptan_polygon.to_file(f"{dl_home}/{area_name}_.geojson",
                           driver='GeoJSON')

    # save the result to a csv file for later reading.
    naptan_polygon.to_csv(f"{dl_home}/{area_name}_polygon.csv",
                          encoding='utf-8',
                          index=False,
                          header=True,
                          sep=',')
    return naptan_polygon


# %%
def dissolve_naptan_boundaries(gdf, dissolve_on='AreaName'):
    """[summary] dissolves a geodataframe of a given subarea, enforces, crs
    type or fails on creation of geodataframe aggregate.

    Args:
        gdf ([type]): [description]
        dissolve_on (str, optional): [description]. Defaults to 'AreaName'.
    """

    # dissolves the given naptan area summing
    gdf_agg = gdf.dissolve(by=dissolve_on,
                           aggfunc='sum').reset_index()
    # keep only the label column and the geometry column.
    gdf_agg = gdf_agg[[f'{dissolve_on}',
                       'geometry']]
    # set the crs value for the aggregated result, here after slimming.
    gdf_agg.crs = {"init": "epsg:4326"}
    # we check that the gdf is still valid, exception triggers if not.
    if gdf_agg.is_valid.all():
        # converts to valid polygon
        # gdf_agg['geometry'] = gdf_agg.geometry.convex_hull
        # if gdf_agg.is_valid.all():
        gdf_agg.to_csv(f"{dl_home}/{dissolve_on}.csv",
                       encoding="utf-8",
                       sep=",")
        return gdf_agg
    else:
        print(f'{dissolve_on} did not dissolve.')


# %%
def make_naptan_polygon_dataset(gdf,
                                naptan_data_level='AreaName',
                                geo_json_name='geo_json_name'):
    """[summary] makes a valid polygon dataset using naptan named areas and
    localities geometry of areas to construct polygons.  

    Args:
        gdf ([geopandas dataframe]): [description]
        area_name ([str]): []
        naptan_column (str, optional): [description]. Defaults to 'LocalityName'.

    Raises:
        NotImplementedError: [description]
        e: [description]

    Returns:
        [type]: [description]
    """

    # check that we can create a polygon out of this.
    # filter dataset to bare minimum needed.
    mask = ~(gdf['Status'] == 'del')
    gdf2 = gdf[mask]
    useful_cols = ["ATCOCode", "NptgLocalityCode", "StopType", "BusStopType",
                   "StopPoint", "LocalityName", "AreaName", "Longitude",
                   "Latitude", 'geometry', 'Status']
    # keep only necessary columns, check we have values for nodes.
    gdf3 = gdf2[useful_cols]

    # check that the area has another nodes to make a polygon.
    if len(gdf3) >= 3:
        # Group by the naptan area level value
        #  1. Get all of the coordinates for that naptan area type as a
        #  list
        #  2. Convert that list to a Polygon
        n_polygon = gdf.groupby('AreaName')['geometry']\
            .apply(lambda x: Polygon(x.tolist())).reset_index()
        # keep exterior points only
        n_polygon['Exterior_Points'] = n_polygon['geometry']\
            .apply(lambda x: Polygon(list(x.exterior.coords)))
        # some renaming is now needed.
        n_polygon = n_polygon.drop(columns=['geometry'])
        n_polygon = n_polygon.rename(columns={"Exterior_Points": "geometry"})
        # save the file output.
        save_polygon_data_format(naptan_polygon=n_polygon,
                                 area_name=geo_json_name,
                                 naptan_column=naptan_data_level)
        return n_polygon
        # TODO - set polygon to just the boundary polygons,
        # TODO - set the polygon to just n percentage
    # else it will be a line string
    elif len(gdf3) == 2:
        # Zip the coordinates into a point object and convert to a
        #  GeoDataFrame
        geometry = [Point(xy) for xy in zip(gdf2.Longitude,
                                            gdf2.Latitude)]
        # fix in
        gdf4 = gpd.GeoDataFrame(gdf3,
                                crs="EPSG:4326",
                                geometry=geometry)
        # Aggregate these points with the GroupBy
        naptan_polygon = gdf4.groupby([naptan_data_level])['geometry']\
            .apply(lambda x: LineString(x.tolist()))
        save_polygon_data_format(naptan_polygon,
                                 area_name=geo_json_name,
                                 naptan_column=naptan_data_level)
        return naptan_polygon
    elif len(gdf3) == 1:
        # TODO -> if a point is given, make a fuzzy polygon area, add a
        #  boundary to the point.
        sys.exit('This is a single point locality and is not supported\
            currently.')
        raise NotImplementedError

    else:
        # get area name of failing areas
        res = gdf3.AreaName.iloc[0]
        sys.exit(f'{res} can not be made into a polygon.')


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

    #
    df_auth = etl_pipe.Create_Naptan_geometry_File(filename)
    #
    df_local = etl_pipe.Create_Locality_Frame(df_auth, locality)
    #
    local_gdf = etl_pipe.Create_GeoDataFrame(df_local)
    #
    parent_Lat, parent_Long = etl_pipe.get_centroid_naptan_area(local_gdf)
    #
    node = local_gdf.loc[local_gdf['ATCOCode'] == atcocode]
    #
    local_gdf = local_gdf[local_gdf.ATCOCode != node.ATCOCode.values[0]]
    #
    node['nearest_geom'] = node.apply(calculate_nearest,
                                      destination=local_gdf,
                                      val=geo,
                                      axis=1)
    #
    node['nearest_node'] = node.apply(calculate_nearest,
                                      destination=local_gdf,
                                      val='ATCOCode',
                                      axis=1)
    #
    nearest_node = local_gdf.loc[local_gdf['ATCOCode']
                                 == node.nearest_node.values[0]]
    #
    local_points = zip(local_gdf.Latitude, local_gdf.Longitude)
    #
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

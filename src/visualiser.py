# %%
import os
import sys
from datetime import datetime
from pathlib import Path

import alphashape
import folium
from folium.plugins import (BeautifyIcon, FloatImage, Fullscreen, HeatMap,
                            MarkerCluster, MeasureControl, Search)
from scipy.spatial import Delaunay
from shapely import wkt
from shapely.geometry import (LineString, MultiPoint, MultiPolygon, Point,
                              Polygon)
from shapely.ops import cascaded_union, unary_union

import etl_pipeline as etl

#homebrew
timestr = datetime.now().strftime("%Y_%m_%d")


# %%
def generate_base_map(gdf):
    """[summary] creates a base map for use in building Naptan maps. 

    Args:
        default_zoom_start (int, optional): [description]. Defaults to 11.

    Returns:
        [type]: [description]
    """
    base_map = folium.Map(location=[gdf['Latitude'].mean(),
                                    gdf['Longitude'].mean()],
                          control_scale=True,
                          prefer_canvas=True,
                          zoom_def=11)
    return base_map


# %%
def display_stop_radius(df, ATCOCode, radius):
    """[summary]- displays a n meters radius around the stop's lat lon coords

    Arguments:
        df {[]} -- [pass dataframe that contains the stop atcocode.]
        stop {[str]} -- [description]
        radius {[type]} -- [description]

    Returns:
        [type] -- [a map type object and saved html interactive map object.]
    """
    try:
        stopID = df.loc[df['ATCOCode'] == ATCOCode]
        name = stopID.CommonName
        lat, lon = stopID.Latitude, stopID.Longitude
        lat_cent, lon_cent = etl.get_centroid_naptan_area(df)
        m = folium.Map(location=[lat_cent, lon_cent],
                       zoom_start=14)
        folium.Marker([lat, lon],
                      popup=(f'<i>{name}</i>'),
                      tooltip=name).add_to(m)
        folium.Circle([lat, lon],
                      radius=radius,
                      popup='Road Radius',
                      fill=True).add_to(m)
        base = (f'{os.getcwd()}/src')
        m.save(f'{base}/output/{ATCOCode}.html')
        return m
    except (IndexError) as e:
        Logger.critical(f'{e}, Value not found in given dataframe.')
    except (ValueError) as e:
        Logger.debug(e)


# %%
def create_concave_polygon(gdf):
    """[summary] Takes in a dataframe sub frame of an area and creates a
    polygon using alphashape, to create a concave_hull of the given area.
    Arguments:
        df {[geopandas]} -- [description]

        alphashape_Value {[int]} -- set to 2.3
                            [the granuality of the concave hull.]
    Returns:
        [shapely.geometry.polygon.Polygon] -- [a shapely polygon, alphashape]
    """
    #  set to 2.3 [the granuality of the concave hull.]
    polygon = alphashape.alphashape(gdf['Geometry'], 2.1)
    return polygon


# %%
def display_locality_polygons(df_sub, naptan_area_level, area_name):
    """[summary] displays all the naptan area polygons, for localities,
    and stop areas from a given dataframe.

    Arguments:
        df_sub {[type]} -- [a sub dataframe level]
        naptan_area_level {[a geopandas data column]} -- [this is the column, we
        are searching within]
        area_names {[string]} -- [name of the area]

    Returns:
        [type] -- [description]
    """
    # TODO make this an empty multipolygon?
    try:
        list_of_polygons = []
        locslist = df_sub[naptan_area_level].unique().tolist()
        for i in locslist:
            subareaframe = etl.create_naptan_subframe(df_sub,
                                                      naptan_area_level,
                                                      i)
            poly = create_concave_polygon(subareaframe)
            list_of_polygons.append(poly)
        union_polygons = unary_union(list_of_polygons)
        return union_polygons
    except Exception as e:
        sys.exit(f'This is a string accessor failure {e}.')


# %%
def visualise_stop_clusters(gdf, display_column, map_name):
    """[summary] use marker clustering to display the large number of nodes,
    Arguments:
        df {[geopandas Dataframe]} -- [Naptan locality dataframe]
        display_column {[pandas series]} -- []
        map_name {[type]} -- [the name of the area to visualise.]
    Returns:
        [folium map object] -- [description]
    """
    # TODO have each different type of stop be represented by a different
    #  colour/ stop icon symbol for the stop point.
    Ferries = ['FTD, FER, FBT']
    Airports = ['AIR, GAT']
    rail_stations = ['RSE, RLY, RPL']
    MetroTram = ['TMU, MET, PLT']
    bus_stations = ['BCE, BST, BCQ, BCS, MKD']
    BusStreet = ['BCT, MKD, CUS, HAR, FLX']
    Taxis = ['TXR']
    Telcabinet = ['LSE, LCB, LPL']
    CarPickup = ['SDA']

    stopTypeColours = {
        "AIR": "red",  # airports
        "GAT": "darkred",  # airport entrances
        # don't use light red, it breaks.
        "FTD": "green",  # ferry entrances
        "FER": "darkgreen",  # ferry access area
        "FBT": "lightgreen",  # ferry bay

        "RSE": "pink",  # railway entrance
        "RLY": "beige",  # railway access area
        "RPL": "lightgray",  # railway pole type

        "BCE": "blue",  # bus entrance
        "BCT": "lightblue",  # bus area
        "BCQ": "darkblue",  # bus bay pole
        "BCS": "cadetblue",  # bus bay pole

        "TXR": "darkpurple",  # taxis
        "SDA": "purple",  # cars drop off pick up
        "LSE": "black"  # telecab
    }

    polys = display_locality_polygons(gdf,
                                      display_column,
                                      map_name)

    # this makes the map and cluster with relational numbers.
    m = generate_base_map(gdf)
    folium.Choropleth(geo_data=polys,
                      data=gdf,
                      columns=['ATCOCode', 'StopType'],
                      legend_name=f'Open Naptan{map_name}',
                      bins=[3, 4, 5, 6, 10],
                      fill_opacity='0.3',
                      fill_color='BuPu',
                      line_opacity=0.3,
                      line_weight='2').add_to(m)
    mc = MarkerCluster().add_to(m)
    """
    feat_group_active = folium.FeatureGroup(name='Active')
    feat_group_unactive = folium.FeatureGroup(name='Unactive')
    marker_cluster_active = MarkerCluster()
    marker_cluster_unactive = MarkerCluster()
    """

    latitudes = list(gdf.Latitude)
    longitudes = list(gdf.Longitude)
    stoppoints = list(gdf.StopPoint)
    stoptypes = list(gdf.StopType)
    nptgcodes = list(gdf.NptgLocalityCode)

    for stoppoint, nptg, stoptype, lat, lon in zip(stoppoints,
                                                   nptgcodes,
                                                   stoptypes,
                                                   latitudes,
                                                   longitudes):

        html = f"""<!DOCTYPE html><div class="boxed">
           <b>StopPoint</b>: <i>{stoppoint}</i><br>
           <b>StopType</b>: {stoptype}<br>
           <b>Locality Code</b>: <i>{nptg}</i><br>
           </div>
                """

        mc.add_child(folium.Marker(location=[lat, lon],
                                   popup=html,
                                   icon=folium.Icon(color='red',
                                                    prefix='fa-',
                                                    icon='ok-sign')))

    # folium.GeoJson(polys, name='Locality Polygons').add_to(m)
    # to allow easier measurement of distance between stops and nodes, 
    # the below control is supplied to draw a line on the map between two
    # points to allow easier checking of distances.
    m.add_child(MeasureControl())
    """ Not implemented currently.
    m.add_child(Search(data=gdf,
                       geom_type='Point',
                       search_label='CommonName'))
    """
    folium.LatLngPopup().add_to(m)
    # folium.LayerControl('topleft', collapsed=True).add_to(m)
    try:
        map_folder = str(os.path.join(Path.home(), "Downloads/Naptan_Maps"))
        Path(f'{map_folder}').mkdir(parents=True,
                                    exist_ok=True)
    except FileExistsError:
        print(f"{map_name} map is being created.")
    else:
        print("Maps folder has been created")
    finally:
        map_dest = f'{map_folder}/{timestr}_{map_name}.html'
        m.save(map_dest)
    return m

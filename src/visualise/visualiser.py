# %%
import os
from os import mkdir
import sys
from datetime import datetime
from pathlib import Path

import folium
from folium.plugins import (
    BeautifyIcon,
    FloatImage,
    Fullscreen,
    HeatMap,
    MarkerCluster,
    MeasureControl,
    Search,
)
from scipy.spatial import Delaunay
from shapely import wkt
from shapely.geometry import LineString, MultiPoint, MultiPolygon, Point, Polygon
from shapely.ops import unary_union
import pandas as pd
import geopandas as gpd

# homebrew
import etl.etl_pipe as etl
import etl.geo_pipe as geo

# homebrew
timestr = datetime.now().strftime("%Y_%m_%d")
dl_home = Path(Path.home() / "Downloads/")
pd.set_option("display.max_rows", 4)


# %%
def style_dictionary():
    """[summary]"""
    #  colour/ stop icon symbol for the stop point.
    Ferries = ["FTD, FER, FBT"]
    Airports = ["AIR, GAT"]
    rail_stations = ["RSE, RLY, RPL"]
    MetroTram = ["TMU, MET, PLT"]
    bus_stations = ["BCE, BST, BCQ, BCS, MKD"]
    BusStreet = ["BCT, MKD, CUS, HAR, FLX"]
    Taxis = ["TXR"]
    Telcabinet = ["LSE, LCB, LPL"]
    CarPickup = ["SDA"]

    # Stop colours and symbols.
    stop_type_colours = {
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
        "LSE": "black",  # telecab
    }
    return stop_type_colours


# %%
def display_locality_polygons(df_sub, naptan_area_level):
    """[summary] displays all the naptan area polygons, for localities,
    and stop areas from a given dataframe.
    Arguments:
        df_sub {[type]} -- [a sub dataframe level]
        naptan_area_level {[a geopandas data column]} -- [this is the column,
        we are searching within]
        area_names {[string]} -- [name of the area]
    Returns:
        [type] -- [description]
    """
    # TODO make this an empty multipolygon?
    try:
        list_of_polygons = []
        locslist = df_sub[naptan_area_level].unique().tolist()
        for i in locslist:
            subareaframe = etl.create_naptan_subframe(df_sub, naptan_area_level, i)
            poly = etl.make_concave_polygon(subareaframe)
            list_of_polygons.append(poly)
        union_polygons = unary_union(list_of_polygons)
        return union_polygons
    except Exception as e:
        sys.exit(f"This is a string accessor failure {e}.")


# %%
def save_generated_map(folium_map, map_name="", map_folder="Downloads/Naptan_Maps"):
    """[summary] Saves map to the specified folder, this is hardcoded to downloads.

    Args:
        folium_map ([html]): [folium map object, the map that has been created.]
        map_name ([str]): [name of the map object being passed]
        map_folder (str, optional): [description]. Defaults to 'Downloads/Naptan_Maps'.

    Returns:
        [type]: [description]
    """
    #
    map_folder = Path(Path.home(), map_folder)
    try:
        # update an existing map.
        print(f"{map_name} map is being updated.")

    #
    except FileNotFoundError:
        Path(f"{map_folder}").mkdir(parents=True, exist_ok=True)
        print("Maps folder has been created.")
    #
    except map_folder.is_dir():
        Path(f"{map_folder}").mkdir(parents=True, exist_ok=True)
    finally:
        print(f"{map_name} map has been created in the map folder.")
        map_dest = f"{map_folder}/{timestr}_{map_name}.html"
        folium_map.save(map_dest)
        return folium_map


# %%


def add_pop_up_data(gdf, map_cluster):
    """[summary] adds the iterative pop ups of each point given to the map
    cluster

    Args:
        gdf ([type]): [description]
        map_cluster ([type]): [description]

    Returns:
        [type]: [description]
    """
    # add the popups with relevant data
    for row in gdf.itertuples():
        html = f"""<!DOCTYPE html><div class="boxed">
            <b>ATCOCode</b>: <i>{row.ATCOCode}</i><br>
            <b>StopType</b>: <i>{row.StopType}</i><br>
            <b>StopPoint</b>: <i>{row.StopPoint}</i><br>
            <b>Coordinates</b>: <i>{row.Latitude}, {row.Longitude}</i><br>
            <b>Locality_Name</b>: {row.LocalityName}<br>
            <b>AreaName</b>: <i>{row.AreaName}</i><br>
            <b>Lower Warnings</b>: {row.Warnings}<br>
            </div>
                """
        # add the markers to the marker cluster.
        folium.Marker(
            location=[row.Latitude, row.Longitude], popup=html, radius=8
        ).add_to(map_cluster)
    return map_cluster


# %%


def generate_base_map(gdf):
    """[summary] creates a base map for use in building Naptan maps.

    Args:
        gdf ([geopandas data]): [description]
        map_name ([str]): [str identify of the map]
    Returns:
        [type]: [description]
    """

    gm = folium.Map(
        location=[gdf["Latitude"].mean(), gdf["Longitude"].mean()],
        zoom_start=11,
        prefer_canvas=True,
        zoom_control=True,
        control_scale=True,
    )
    #  add measure control with km and area return calculations.
    gm.add_child(
        MeasureControl(
            position="bottomright",
            primary_length_unit="kilometers",
            secondary_length_unit="miles",
            secondary_area_unit="acres",
            primary_area_unit="sqmeters",
        )
    )
    # added lat long pop up for reference
    folium.LatLngPopup().add_to(gm)
    # clustering added
    mc = MarkerCluster().add_to(gm)

    # add the popups with relevant data
    for row in gdf.itertuples():
        html = f"""<!DOCTYPE html><div class="boxed">
                <b>ATCOCode:</b> <i>{row.ATCOCode}</i><br>
                <b>StopType:</b> <i>{row.StopType}</i><br>
                <b>StopPoint:</b> <i>{row.StopPoint}</i><br>
                <b>Coordinates:</b> <i>{row.Latitude}, {row.Longitude}</i><br>
                <b>Locality_Name:</b> {row.LocalityName}<br>
                <b>AreaName:</b> <i>{row.AreaName}</i><br>
                </div>
                """
        # add the markers to the marker cluster.
        mc.add_child(
            folium.Marker(
                location=[row.Latitude, row.Longitude],
                popup=html,
                radius=8,
                icon=folium.Icon(color="green", prefix="fa-", icon="ok-sign"),
            )
        )
    # add layer control.
    folium.LayerControl(collapsed=False, position="topright").add_to(gm)
    # get name of the mapped area.
    map_name = gdf.AreaName.iloc[0]
    # save the map
    save_generated_map(mc, map_name=map_name)
    return gm


# %%
def generate_sample_map(gdf, failed_nodes, col_name, col_value):
    """[summary] when given a geodataframe of failed nodes, will create a
    map of represenative sampling of the failed nodes for a given test.
    This is to prevent creating maps that have 30,000+ nodes from being
    created as this will cause  displaying.

    Args:
        gdf ([type]): [the naptan master dataframe]
        failed_node ([type]): [the dataframe of failed nodes]
        col_name ([str]): [pandas column name.]
        col_name ([str]): [the value sought in the above named column.]
    """
    # this gives us a dataframe for each of the unique values found in failed
    #  nodes column
    short_codes = failed_nodes[failed_nodes[f"{col_name}"] == col_value]
    # this give us a sample number to use
    sample_rate = round(len(gdf) / len(short_codes) * 100)
    short_codes = short_codes.sample(sample_rate)
    # the function will save the map
    m = generate_base_map(short_codes, f"{col_name}", col_value)
    return m


# %%
def simple_map(gdf, name):
    """[summary]

    Args:
        gdf ([type]): [description]
        name ([type]): [description]
    """
    sm = folium.Map(
        Location=[gdf.Latitude.mean(), gdf.Longitude.mean()], zoom_start=10, name=name
    )
    for row in gdf.itertuples():
        folium.Marker(
            location=[row.Latitude, row.Longitude], popup=row.name, radius=8
        ).add_to(sm)
    gdf


# %%
def calculate_stop_areas(gdf, stop_area_parent):
    """[summary] we need to group the stop areas togethers into dataframes that
    let us group them together so we can work out what our areas look like as
    polygons.

    Args:
        gdf ([type]): [description]
        stop_area_parent ([type]): [description]

    Returns:
        [type]: [description]
    """
    # TODO group stop areas into individual dataframes,
    # TODO make them into polygons,
    nodes = etl.create_naptan_subframe(gdf, "AreaName", stop_area_parent)
    cols = [
        "ATCOCode",
        "Latitude",
        "Longitude",
        "StopAreaName",
        "StopAreaCode",
        "StopAreaType",
        "Latitude_area",
        "Longitude_area",
        "geometry",
    ]
    mask = ~(nodes["Status_area"] == "del")
    nodes = nodes[mask]
    #  count number of stop areas in the admin area
    nodes = nodes[nodes["StopAreaName"].notna()]
    # we group together to create a dataframe of the stop area name and by type
    # we filtered out any stops which don't have at least 3 points, 2 is
    # a line, so that will be a problem for later.
    group_nodes = (
        nodes[cols]
        .groupby(["StopAreaName"])
        .filter(lambda g: len(g) >= 3)
        .reset_index(drop=True)
    )
    # we need the names of each unique stop area.
    stop_area_unique = group_nodes["StopAreaName"].unique()
    # we get a dataframe counting out stop areas.
    # group_nodes.describe()[['count']].reset_index()
    stop_area_polys = []
    multi_polygons = []
    # This generates the stop area polygons as generator objects in a list,
    # which is a good, but we have the issue of how do we compare generator
    # objects to one another.
    group_nodes_selected = group_nodes.groupby(["StopAreaName"])
    for sau in stop_area_unique:
        g_nodes = group_nodes_selected.get_group(sau)
        gdf1 = gpd.GeoDataFrame(g_nodes, columns=cols)
        etl.folder_creator(Path(f"{os.getcwd()}/_stop_area_cache_/"))
        stop_area_polys.append(gdf1)
        gdf1.to_csv(
            f"{os.getcwd()}/sample/{sau}.csv",
            sep=",",
            mode="w",
            encoding="utf-8",
            index=True,
            header=True,
        )

    for sau in stop_area_unique:
        #  we get the groups
        g_nodes = group_nodes_selected.get_group(sau)
        # reset our indexes just to be safe.
        g_nodes.set_index("StopAreaCode", inplace=True)
        g_nodes.sort_index(inplace=True)
        # compress geoseries to geometry column, no need of anything else
        points = g_nodes["geometry"]
        # map out the coordinates sequences.
        coords = [p.coords[:][0] for p in points]
        # add them to a polygon object.
        multi_polygons = Polygon(coords)

    return stop_area_polys, multi_polygons


"""
kent = etl.create_naptan_subframe(gdf, 'AreaName', 'kent')
stop_areas, mps = calculate_stop_areas(kent, 'kent')
mps
stop_areas
"""

# %%
def make_map(gdf):
    gm = folium.Map(
        location=[gdf["Latitude"].mean(), gdf["Longitude"].mean()],
        zoom_start=11,
        prefer_canvas=True,
        zoom_control=True,
        control_scale=True,
    )
    #  add measure control with km and area return calculations.
    gm.add_child(
        MeasureControl(
            position="bottomright",
            primary_length_unit="kilometers",
            secondary_length_unit="miles",
            secondary_area_unit="acres",
            primary_area_unit="sqmeters",
        )
    )
    # added lat long pop up for reference
    folium.LatLngPopup().add_to(gm)
    # clustering added
    mc = MarkerCluster().add_to(gm)

    # add the popups with relevant data
    for row in gdf.itertuples():
        html = f"""<!DOCTYPE html><div class="boxed">
                <b>ATCOCode:</b> <i>{row.ATCOCode}</i><br>
                <b>StopType:</b> <i>{row.StopType}</i><br>
                <b>StopPoint:</b> <i>{row.StopPoint}</i><br>
                <b>Coordinates:</b> <i>{row.Latitude}, {row.Longitude}</i><br>
                <b>Locality_Name:</b> {row.LocalityName}<br>
                <b>AreaName:</b> <i>{row.AreaName}</i><br>
                </div>
                """
        # add the markers to the marker cluster.
        mc.add_child(
            folium.Marker(
                location=[row.Latitude, row.Longitude],
                popup=html,
                radius=8,
                icon=folium.Icon(color="green", prefix="fa-", icon="ok-sign"),
            )
        )
    # add layer control.
    folium.LayerControl(collapsed=False, position="topright").add_to(gm)

    return gm


# make_map(yorkshire)

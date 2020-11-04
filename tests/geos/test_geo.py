# %%
# geo_tests.py
# %%
import geos
import unittest
from unittest.mock import MagicMock, Mock
import pytest
import pandas as pd
from numpy import testing
import numpy as np
import os
os.getcwd()


def test_calculate_nearest():
    """[summary]
    """
    assert geos.calculate_nearest()


def test_check_naptan_area_shape():
    """[summary]
    """
    assert geos.check_naptan_area_shape()


def test_check_polygon_longests():
    """[summary]
    """
    assert geos.check_polygon_longests()


def test_check_polygons_intersect():
    """[summary]
    """
    assert geos.check_polygons_intersect()


def test_get_nearest_road_name():
    """[summary]
    """
    assert geos.get_nearest_road_name()


def test_naptan_coastal_nodes():
    """[summary]
    """
    assert geos.naptan_coastal_nodes()


def test_nearest_naptan_stop():
    """[summary]
    """
    assert geos.nearest_naptan_stop()


def test_nearest_points():
    """[summary]
    """
    assert geos.nearest_points()


def test_node_distance():
    assert geos.node_distance()


def test_check_area_length_is_regular():
    """[summary]
    """
    assert geos.check_area_length_is_regular()


def test_road_name_matches_coordinates():
    """[summary]
    """
    assert geos.road_name_matches_coordinates()


def test_stop_proximity():
    """[summary]
    """
    assert geos.stop_proximity()


def test_stops_in_different_authority_geo_position():
    """[summary]
    """
    assert geos.stops_in_different_admin_authority_geo_position()


def test_stops_with_wrong_bearing():
    """[summary]
    """
    assert geos.stops_with_wrong_bearing()


if __name__ == "__main__":
    unittest.main()

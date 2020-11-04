# %% etl.py
# %%
from src.etl import etl_pipe as etl
from unittest.mock import MagicMock, Mock, TestCase
import warnings
import pytest
import pandas as pd
from pandas.testing import (
    assert_frame_equal, assert_index_equal, assert_series_equal)
from numpy import testing
import numpy as np
import os
os.getcwd()


# %%
@pytest.fixture
def test_downloads_naptan_data():
    """[summary]
    """

    assert etl.downloads_naptan_data()


def test_extract_naptan_files():
    """[summary]
    """
    assert etl.extract_naptan_files()


def test_check_naptan_files():
    """[summary]
    """
    assert etl.check_naptan_files()


def test_convert_to_lat_long():
    """[summary]
    """
    etl.convert_to_lat_long()


def test_calculate_naptan_geometry():
    """[summary]
    """
    etl.calculate_naptan_geometry()


class test_deactivated_nodes(TestCase):

    def test_deactivated_nodes_exist():
        """[summary]
        """
        etl.deactivated_nodes()

    def test_removal_deactived_nodes():
        """
        """
        assert pd.testing.


def test_read_naptan_file():
    """[summary]
    """
    etl.read_naptan_file()


def test_non_standard_stop_area_generation():
    """[summary]
    """
    etl.non_standard_stop_area_generation()


def test_get_centroid_naptan_area():
    """[summary]
    """
    etl.get_centroid_naptan_area()


def test_get_groupby_admin_area_common_value():
    """[summary]
    """
    etl.get_groupby_admin_area_common_value()


def test_naptan_gazette_admin_area_codes():
    """[summary]
    """
    etl.naptan_gazette_admin_area_codes()


def test_naptan_gazette_districts():
    """[summary]
    """
    etl.naptan_gazette_districts()


def test_naptan_gazette_localities():
    """[summary]
    """
    etl.naptan_gazette_localities()


def test_naptan_gazette_region():
    """[summary]
    """
    etl.naptan_gazette_region()


def test_map_gazette_to_nodes():
    """[summary]
    """
    etl.map_gazette_to_nodes()


def test_merge_stop_areas():
    """[summary]
    """
    etl.merge_stop_areas()


def test_create_naptan_subframe():
    """[summary]
    """
    etl.create_naptan_subframe()
# %%

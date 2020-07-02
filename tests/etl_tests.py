# etl_tests.py
import unittest
import etl_pipeline as etl
from unittest.mock import MagicMock, Mock


class ETLTestSolver(unittest.TestCase):
    """[summary]

    Args:
        unittest ([type]): [description]
    """

    def downloads_naptan_data_tests(self):
        """[summary]
        """
        etl.downloads_naptan_data()

    def extract_naptan_files_tests(self):
        """[summary]
        """
        etl.extract_naptan_files()

    def check_naptan_files_tests(self):
        """[summary]
        """
        etl.check_naptan_files()

    def convert_to_lat_long_tests(self):
        """[summary]
        """
        etl.convert_to_lat_long()

    def calculate_naptan_geometry_tests(self):
        """[summary]
        """
        etl.calculate_naptan_geometry()

    def deactivated_nodes_tests(self):
        """[summary]
        """
        etl.deactivated_nodes()

    def read_naptan_file_tests(self):
        """[summary]
        """
        etl.read_naptan_file()

    def non_standard_stop_area_generation_tests(self):
        """[summary]
        """
        etl.non_standard_stop_area_generation()

    def get_centroid_naptan_area_tests(self):
        """[summary]
        """
        etl.get_centroid_naptan_area()

    def get_groupby_admin_area_common_value_tests(self):
        """[summary]
        """
        etl.get_groupby_admin_area_common_value()

    def naptan_gazette_admin_area_codes_tests(self):
        """[summary]
        """
        etl.naptan_gazette_admin_area_codes()

    def naptan_gazette_districts_tests(self):
        """[summary]
        """
        etl.naptan_gazette_districts()

    def naptan_gazette_localities_tests(self):
        """[summary]
        """
        etl.naptan_gazette_localities()

    def naptan_gazette_region_tests(self):
        """[summary]
        """
        etl.naptan_gazette_region()

    def map_gazette_data_to_nodes_tests(self):
        """[summary]
        """
        etl.map_gazette_data_to_nodes()

    def create_stop_areas_tests(self):
        """[summary]
        """
        etl.create_stop_areas()

    def create_naptan_subframe_tests(self):
        """[summary]
        """
        etl.create_naptan_subframe()

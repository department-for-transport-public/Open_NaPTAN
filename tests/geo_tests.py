#geo_tests.py
import unittest
import geo_checks as geo
from unittest.mock import MagicMock, Mock


class GeoTestSolver(unittest.TestCase):
    """[summary]

    Args:
        unittest ([type]): [description]
    """

    def calculate_nearest_tests(self):
        """[summary]
        """
        geo.calculate_nearest

    def check_naptan_area_shape_tests(self):
        """[summary]
        """
        geo.check_naptan_area_shape

    def check_polygon_lengths_tests(self):
        """[summary]
        """
        geo.check_polygon_lengths

    def check_polygons_intersect_tests(self):
        """[summary]
        """
        geo.check_polygons_intersect

    def get_nearest_road_name_tests(self):
        """[summary]
        """
        geo.get_nearest_road_name

    def naptan_coastal_nodes_tests(self):
        """[summary]
        """
        geo.naptan_coastal_nodes

    def nearest_naptan_stop_tests(self):
        """[summary]
        """
        geo.nearest_naptan_stop

    def nearest_points_tests(self):
        """[summary]
        """
        geo.nearest_points

    def node_distance_tests(self):
        geo.node_distance

    def polygon_length_is_regular_tests(self):
        """[summary]
        """
        geo.polygon_length_is_regular

    def road_name_matches_coordinates_tests(self):
        """[summary]
        """
        geo.road_name_matches_coordinates

    def stop_proximity_tests(self):
        """[summary]
        """
        geo.stop_proximity

    def stops_in_different_authority_geo_position_tests(self):
        """[summary]
        """
        geo.stops_in_different_admin_authority_geo_position()

    def stops_with_wrong_bearing_tests(self):
        """[summary]
        """
        geo.stops_with_wrong_bearing


if __name__ == "__main__":
    unittest.main()

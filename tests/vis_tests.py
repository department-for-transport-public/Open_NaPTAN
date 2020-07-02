# vis_tests.py
import unittest
import visualiser as vis
from unittest.mock import MagicMock, Mock


class VisTestSolver(unittest.TestCase):
    """[summary]

    Args:
        unittest ([type]): [description]
    """

    def create_concave_polygon_tests(self):
        """[summary]
        """
        vis.create_concave_polygon()
        pass

    def display_locality_polygons_tests(self):
        """[summary]
        """
        vis.display_locality_polygons()
        pass

    def display_stop_radius_tests(self):
        """[summary]
        """
        vis.display_stop_radius()
        pass

    def generate_base_map_tests(self):
        """[summary]
        """
        vis.generate_base_map()
        pass

    def visualise_stop_clusters_tests(self):
        """[summary]
        """
        vis.visualise_stop_clusters()
        pass

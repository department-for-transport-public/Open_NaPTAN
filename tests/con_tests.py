# con_tests.py
import unittest
import con_checks as con
from unittest.mock import MagicMock, Mock


class ConTestSolver(unittest.TestCase):
    """[summary]

    Args:
        unittest ([type]): [description]
    """

    def check_name_too_long_tests(self):
        """[summary]
        """
        con.check_name_too_long()

    def define_stops_areas_tests(self):
        """[summary]
        """
        con.define_stops_areas()

    def localities_with_identical_stops_tests(self):
        """[summary]
        """
        con.localities_with_identical_stops()

    def node_has_repeating_word_tests(self):
        """[summary]
        """
        con.node_has_repeating_word()

    def remove_illegal_caps_tests(self):
        """[summary]
        """
        con.remove_illegal_caps()

    def remove_illegal_chars_tests(self):
        """[summary]
        """
        con.remove_illegal_chars()

    def remove_illegal_spaces_tests(self):
        """[summary]
        """
        con.remove_illegal_spaces()

    def stop_name_contains_locality_name_tests(self):
        """[summary]
        """
        con.stop_name_contains_locality_name()

    def stop_names_with_high_risk_words_tests(self):
        """[summary]
        """
        con.stop_names_with_high_risk_words()

    def stop_with_bearing_missing_tests(self):
        """[summary]
        """
        con.stop_with_bearing_missing()

    def stop_with_multiple_road_names_tests(self):
        """[summary]
        """
        con.stop_with_multiple_road_names()

    def stops_in_different_admin_area_tests(self):
        """[summary]
        """
        con.stops_in_different_admin_area()

    def stops_area_members_without_identical_names_tests(self):
        """[summary]
        """
        con.stops_area_members_without_identical_names()

    def stops_in_alternate_localities_tests(self):
        """[summary]
        """
        con.stops_in_alternate_localities()

    def locality_not_unique_tests(self):
        """[summary]
        """
        con.locality_not_unique()

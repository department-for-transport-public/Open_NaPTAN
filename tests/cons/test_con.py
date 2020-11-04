# con_tests.py
import unittest

# %%
from cons import (localities_with_identical_stops,
                  check_illegal_caps,
                  check_illegal_chars,
                  check_illegal_spaces,
                  stop_with_bearing_missing,
                  stop_name_contains_locality_name,
                  check_name_length,
                  stop_names_with_high_risk_words,
                  stop_with_multiple_road_names)

from unittest.mock import MagicMock, Mock
import pytest
import pandas as pd
from numpy import testing
import numpy as np
import os
os.getcwd()


# %%
@ pytest.fixture
def test_check_name_too_long():
    """[summary]
    """
    check_name_length()


def test_check_name_too_short():
    check_name_length()


def test_check_name_is_3_parts():
    """ check that the stop name, common name, locality name are in the name.
    """
    check_name_length()


def test_define_stops_areas():
    """[summary]
    """
    define_stops_areas()


def test_localities_with_identical_stops():
    """[summary]
    """
    cons.localities_with_identical_stops()


def test_node_has_repeating_word():
    """[summary]
    """
    cons.node_has_repeating_word()


def test_check_illegal_caps():
    """[summary]
    """
    check_illegal_caps()


def test_check_illegal_chars():
    """[summary]
    """
    check_illegal_chars()


def test_check_illegal_spaces():
    """[summary]
    """
    check_illegal_spaces()


def test_stop_name_contains_locality_name():
    """[summary]
    """
    stop_name_contains_locality_name()


def test_stop_names_with_high_risk_words():
    """[summary]
    """
    stop_names_with_high_risk_words()


def test_stop_with_bearing_missing():
    """[summary]
    """
    stop_with_bearing_missing()


def test_stop_with_multiple_road_names():
    """[summary]
    """
    stop_with_multiple_road_names()


def test_stops_in_different_admin_area():
    """[summary]
    """
    stops_in_different_admin_area()


def test_stops_area_members_without_identical_names():
    """[summary]
    """
    stops_area_members_without_identical_names()


def test_stops_in_alternate_localities():
    """[summary]
    """
    stops_in_alternate_localities()


def test_locality_not_unique():
    """[summary]
    """
    locality_not_unique()


if __name__ == '__main__':
    unittest.main()

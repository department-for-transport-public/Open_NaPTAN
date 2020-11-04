# vis_tests.py
from src.visualise import visualiser as vis
import unittest
from unittest.mock import MagicMock, Mock
import pytest
import pandas as pd
from numpy import testing
import numpy as np
import os
os.getcwd()

# %%


def test_style_dictionary():
    """
    """
    # TODO - check that the style dictionary correctly displays the right color
    # for the right stop
    assert vis.style_dictionary()


def test_create_concave_polygon():
    """[summary]
    """
    assert vis.create_concave_polygon()
    pass


def test_display_locality_polygons():
    """[summary]
    """
    assert vis.display_locality_polygons()
    pass


def test_display_stop_radius():
    """[summary]
    """
    vis.display_stop_radius()
    pass


def test_generate_base_map():
    """[summary]
    """
    vis.generate_base_map()
    pass

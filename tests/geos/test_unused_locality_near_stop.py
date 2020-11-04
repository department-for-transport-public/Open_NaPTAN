from geos import unused_locality_near_stops as unused
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def test_unused_locality_near_stops_99_meters():
    """[summary]
    """
    assert unused()


def test_unused_locality_near_stops_has_no_stops():
    """[summary]
    """
    assert unused()


def test_unused_locality_near_stops_has_no_child_localities():
    """[summary]
    """
    assert unused()


def test_unused_locality_near_stops_has_neighbour_localities():
    """[summary]
    """
    assert unused()


def test_unused_locality_near_stops_has_nptg_entries():
    """[summary] test that the stops' locality has an nptg entry
    """
    assert unused()


@pytest.mark.xfail(reason="if a locality is 150 meters or more away from the stop then it should fail this test, as the locality is far enough away.")
def test_unused_locality_near_stops_150_meters():
    """[summary] test the response is 150 or more meters from the stop
    """
    assert unused()

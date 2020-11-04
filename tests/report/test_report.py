# %%
# report_tests.py
from report import reporting as rep
from etl.etl_pipe import folder_creator
import unittest
from unittest.mock import MagicMock, Mock
import pytest
import pandas as pd
from numpy import testing
import numpy as np
from datetime import datetime
import os
from pathlib import Path
os.getcwd()

# get download path
timestr = datetime.now().strftime("%Y_%m_%d")
dl = Path(Path.home() / 'Downloads/')
# %%


@pytest.fixture
def naptan_sample():
    """[summary]
    """
    # what
    t = rep.report_failing_nodes()
    return t


def test_report_failing_nodes(naptan_sample):
    """[summary]
    """
    assert naptan_sample.report_failing_nodes()
    assert rep.report_failing_nodes(complete_gdf,
                                    'Check Name Length',
                                    gdf)


def test_error_folder_created():
    """[summary]
    """

    assert folder_creator(
        f'{dl}/Naptan_Error_Reports/{timestr}/') == f'{dl}/Naptan_Error_Reports/{timestr}/'


def test_error_report_created():
    """[summary]
    """
    pass


def test_plot_missing_data():
    """[summary]
    """
    rep.plot_missing_data()


def test_list_unique_values():
    """[summary]
    """
    assert rep.list_unique_values()


def test_print_column_info():
    """[summary]
    """
    assert rep.print_column_info()


def test_visualise_missing_counts():
    """[summary]
    """
    assert rep.visualise_missing_counts()

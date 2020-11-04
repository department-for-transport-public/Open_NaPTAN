from _pytest.outcomes import fail
from cons.naptan_data_structure import NaptanStructureChecks
import pytest
import unittest
import pandas as pd
import pandas.testing
import numpy as np
from cons.naptan_data_structure import NaptanStructureChecks as Structure
from numpy.testing import assert_approx_equal, assert_raises, dec, assert_


@pytest.mark.usefixtures()
class NaptanStructureTests(unittest.TestCase):
    """[summary]
    """

    @dec.slow
    def test_naptan_structure_stop_number_limits_upper():
        """[summary] test the upper limit

        Args:
            py ([type]): [description]
        """
        gdf_test =
        Structure.check_naptan_stop_number_limits()

    def test_naptan_structure_stop_number_limits_lower():
        """[summary] check that the lower limit is fine
        """
        assert Structure.check_naptan_stop_number_limits()

    @pytest.mark.fail
    def test_invalid_parameters():
        """[summary]
        """
        assert_raises()

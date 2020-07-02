#main_test.py
import unittest
import main
from unittest.mock import MagicMock, Mock


class TestSolver(unittest.TestCase):
    """[summary]

    Args:
        unittest ([type]): [description]
    """

    def etl_integration(self):
        main.load_naptan_data()
        pass

    def con_check_integration(self):
        pass

    def geo_check_integration(self):
        pass

    def report_integration(self):
        pass

    def visualiser_integration(self):
        pass


if __name__ == "__main__":
    unittest.main()

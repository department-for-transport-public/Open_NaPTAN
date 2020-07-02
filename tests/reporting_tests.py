# report_tests.py
import unittest
import reporting as report
from unittest.mock import MagicMock, Mock


class ReportTestSolver(unittest.TestCase):
    """[summary]

    Args:
        unittest ([type]): [description]
    """

    def nodes_error_reporting_tests(self):
        """[summary]
        """
        report.nodes_error_reporting()

        def error_folder_created(self):
            """[summary]
            """
            pass

        def error_report_created(self):
            """[summary]
            """
            pass

    def plot_missing_data_tests(self):
        """[summary]
        """
        report.plot_missing_data()

    def list_unique_values_tests(self):
        """[summary]
        """
        report.list_unique_values()

    def print_column_info_tests(self):
        """[summary]
        """
        report.print_column_info()

    def visualise_missing_counts_tests(self):
        """[summary]
        """
        report.visualise_missing_counts()

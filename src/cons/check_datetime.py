from datetime import datetime, date, time, timedelta
from checks import NaptanCheck
from report.reporting import report_failing_nodes
import pandas as pd
import numpy as np


class CheckDateTime(NaptanCheck):
    """[summary] a collection of methods to check the internal consistency of
    the date and time entries stored.

    Args:
        NaptanCheck ([type]): [description]

    Returns:
        [type]: [description]
    """

    @classmethod
    def check_stop_dates_not_after_today(cls, gdf):
        """[summary] checks if the dates for bus stops have not been
        added to the naptan database in a future date.

        Args:
            gdf ([type]): [description]
            check_name ([type]): [description]
            check_warning_level ([type]): [description]
            check_geographical_level ([type]): [description]

        Returns:
            [type]: [description]
        """

        check_name = "Check stop dates are after today"
        check_geographic_level = "stop"
        check_warning_level = "low"

        # just use between for both date fields.
        today = pd.Timestamp(datetime.today().date())
        # check if greater than today in mod date column
        baddates = gdf[gdf.ModificationDateTime > today]
        # mask for speed.
        bad_timeframe = baddates
        # check if we report.
        if bad_timeframe.empty:
            print("No stop dates are in the future.")
        else:
            print(f"Stop creation or modification date after {today}.")
            report_failing_nodes(gdf, check_name, bad_timeframe)
            return bad_timeframe

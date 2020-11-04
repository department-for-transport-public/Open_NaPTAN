from checks import NaptanCheck
import geopandas as gpd
import pandas as pd
import numpy as np
from report import reporting as rep


# %%

class StopsAreaNameChecks(NaptanCheck):
    """[StopArea containing StopPoints that do not have identical CommonNames]
    Args:
        NaptanCheck ([type]): [description]
    """
    check_geographic_level = 'stop areas'
    check_name = 'StopArea StopPoints do not have identical CommonNames'
    check_warning_level = 'medium'

    @classmethod
    def stops_area_members_without_identical_names(cls, gdf):
        """[summary] StopArea containing StopPoints that do not have identical
        CommonNames


        Args:
            gdf ([type]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        check_name = "stops_area_members_without_identical_names"
        gdf1 = gdf
        failed_nodes = ''
        rep.report_failing_nodes(gdf, check_name, failed_nodes)
        return failed_nodes
        raise NotImplementedError

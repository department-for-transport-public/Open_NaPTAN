import sys
from report import reporting as rep

from src.checks import NaptanCheck

# %%


class BearingMissing(NaptanCheck):
    """[summary]

    Args:
        NaptanCheck ([type]): [description]
    """
    # for reporting
    check_name = 'Check stop bearing missing.'
    check_warning_level = 'high'
    check_geographic_level = 'stop'

    @classmethod
    def stop_with_bearing_missing(cls, gdf):
        """[summary] The data does not include a value for “bearing” for all BCT
        stops except those in the FLX (flexible zone) sub-type.

        Args:
            gdf {[geopandas dataframe]} -- [The naptan master dataframe.]

        Returns:
            [type]: [description]
        """
        # get the check name
        check_name = 'stop_with_bearing_missing'
        try:
            # the permitted bearings that can be present in that field.
            valid_bearing = ['SW', 'NE', 'SE', 'S', 'N', 'NW', 'E', 'W']
            # merged form, checking for the validing bearing list is not
            # present
            failed_nodes = gdf[(gdf['StopType'] == 'BCT') &
                               (gdf['BusStopType'] != 'FLX') &
                               (~gdf['Bearing'].isin(valid_bearing))]
            # reporting.
            rep.report_failing_nodes(gdf,
                                     check_name,
                                     failed_nodes)
            return failed_nodes
        except Exception as e:
            sys.exit(f'{check_name} has failed because of {e}')

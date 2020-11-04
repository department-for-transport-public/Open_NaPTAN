import sys
from report import reporting as rep
from checks import NaptanCheck

# %%


class CheckName(NaptanCheck):
    """[summary] A collectin of methods for handling issues for checking names
    within the naptan dataset.
    """

    # for reporting
    check_name = "Check Name Length"
    check_warning_level = "High"
    check_geographic_level = "stop"

    @classmethod
    def check_name_length(cls, gdf):
        """[summary]:- A stop point fails if StopPoint has a full name [Locality,
        CommonName (Indicator)] that is more than 80 characters in length.

        Arguments:
            gdf {[geopandas dataframe]} -- [The naptan master dataframe.]
        Returns:
            df_str {[dataframe of ]} -- Nodes that failed the check.
        """
        try:
            # get name for report
            check_name = "check_name_length"
            # clean frame
            gdf1 = gdf
            # get the stoppoint name
            gdf1["newName"] = (
                gdf1["CommonName"].astype(str) + ", " + gdf1["LocalityName"].astype(str)
            )
            # mask the names against 80 chars
            mask = gdf1["newName"].str.len() > 80
            df_str = gdf1.loc[mask]
            # send to report
            rep.report_failing_nodes(gdf, check_name, df_str)
            return df_str.ATCOCode
        except Exception as e:
            raise e
            sys.exit(f"{check_name} failed because of {e}.")

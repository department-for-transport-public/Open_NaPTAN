import pandas as pd
from report import reporting as rep
from checks import NaptanCheck
import sys

# %%


class StopsDifferentNamedAdminArea(NaptanCheck):
    """[summary]

    Args:
        NaptanCheck ([type]): [description]
    """

    # for reporting
    check_name = "stops_in_different_admin_area"
    check_warning_level = "high"
    check_geographic_level = "stop"

    @classmethod
    def stops_in_different_admin_area(cls, gdf):
        """[summary] Checks if a stop is in a different administrative area, based
        on the AtcoAreaCode Column. We take the first 3 characters prefix of the
        atcocode and check them against the atcoareacode for the admin area.
        They should match.
        Args:
            gdf ([pandas dataframe]): [The Master naptan node frame.]
        Returns:
            [panda dataframe] -- [description]
        Raises:
            NotImplementedError: [geo spatial cross checking, not implemented yet.]
        """
        check_name = "stops_in_different_admin_area"
        gdf1 = gdf
        try:
            #  get prefix from atcocode column
            gdf1["atcocodeprefix"] = gdf1["ATCOCode"].str[:3]
            #  get the AtcoAreaCode column value, making sure that we account for
            # 2-digit atcocode prefixes and int types, using to_numeric
            gdf1["AtcoAreaCode"] = gdf1["AtcoAreaCode"].astype(str)
            gdf1["atcocodeprefix"] = pd.to_numeric(gdf1["atcocodeprefix"])
            gdf1["AtcoAreaCode"] = pd.to_numeric(gdf1["AtcoAreaCode"])
            #  compare the two together, they should match
            gdf1["not matching"] = gdf1["atcocodeprefix"].eq(
                pd.to_numeric(gdf1["AtcoAreaCode"], errors="coerce")
            )
            failed_nodes = gdf1[~gdf1["not matching"]]
            rep.report_failing_nodes(gdf, check_name, failed_nodes)
            return failed_nodes
            # TODO if they don't match, report the nodes that don't match
            # TODO compare the geometry point to the polygon boundaries of the
            #  expected admin area
            # TODO if the geometry point is further 500 meters outside the
            #  boundaries of the given area, then the node fails
        except Exception as e:
            raise e
            sys.exit(f"{check_name} has failed because of {e}")

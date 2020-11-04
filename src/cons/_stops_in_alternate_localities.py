import sys
from etl import etl_pipe
from report import reporting as rep
from visualise.visualiser import generate_base_map

from checks import NaptanCheck

# %%


class StopsAlternativeLocality(NaptanCheck):
    """[summary] Locality is an alternative but has members or children that
     should be connected to the primary Locality.


    Args:
        NaptanCheck ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """

    # for reporting
    check_name = "Check Illegal Characters"
    check_warning_level = "Medium"
    check_geographic_level = "stop"

    @classmethod
    def stops_in_alternate_localities(cls, gdf):
        """[summary] Locality is an alternative but has members or children
         that should be connected to the primary Locality. This checks if the
         stop can be linked to an nptg locality.


        Args:
            gdf ([type]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        check_name = "stops_in_alternate_localities"
        gdf1 = gdf
        failed_nodes = ""
        rep.report_failing_nodes(gdf, check_name, failed_nodes)
        return failed_nodes
        raise NotImplementedError

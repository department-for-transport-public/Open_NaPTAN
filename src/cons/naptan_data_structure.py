from checks import NaptanCheck
from report.reporting import report_failing_nodes, write_basic_log_file
import sys


class NaptanStructureChecks(NaptanCheck):
    """[summary] a collection of basic sanity checks, to ensure that the naptan
    data is loaded successfully from source. If any of these fail it
    constitues a critical failure of naptan structure.

    Args:
        NaptanCheck ([type]): [description]
    """

    check_geographic_level = "national"
    check_name = "Check naptan structure levels"
    check_warning_level = "Critical"

    @classmethod
    def check_naptan_stop_number_limits(cls, gdf, low_limit=375000, upper_limit=460000):
        """[summary] we check the number of stops/ rows in the completely
         downloaded naptan data is within acceptable ranges.

        Args:
            gdf ([type]): [description]
            low_limit (int, optional): [description]. Defaults to 375000.
            upper_limit (int, optional): [description]. Defaults to 460000.
        """
        # check the number of rows is sufficient for naptan purposes.
        if gdf.shape[0] <= low_limit:
            # if the number of naptan checks drops by the
            message = f"The number of naptan stops has dropped  \
                {low_limit - gdf.shape[0]}."
            write_basic_log_file(message)
            sys.exit(f"{message}")
        elif gdf.shape[0] >= upper_limit:
            # check it is not over a sensible threshold
            message = f"The number of naptan stops has risen unexpectedly \
                 {gdf.shape[0] - upper_limit}."
            write_basic_log_file(message)
            sys.exit(f"{message}")
        else:
            print(f"{gdf.shape[0]} number of rows is within acceptable limits.")
            pass

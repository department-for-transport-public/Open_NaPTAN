from report import reporting as rep
from checks import NaptanCheck

# %%


class BusStopTypeWrong(NaptanCheck):
    """[summary] StopPoint has a 'BCS' Stop Type but is not in a Bus Station Stop Area


    Args:
        NaptanCheck ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """

    check_name = "Bus stop wrong type."
    check_geographic_level = "stop"
    check_warning_level = "low"

    @classmethod
    def get_distance(cls, parameter_list):
        """
        docstring
        """
        pass

    @classmethod
    def stop_with_wrong_types(cls, gdf):
        """[summary]

        Args:
            gdf ([type]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        check_name = "stop_with_wrong_types"
        # list of stops not in correct admin areas by geo position.
        failed_nodes = ""
        rep.report_failing_nodes(gdf, check_name, failed_nodes)
        return failed_nodes
        raise NotImplementedError

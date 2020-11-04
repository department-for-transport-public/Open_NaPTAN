from checks import NaptanCheck
from report import reporting as rep

# %%


class StopRoadDistance(NaptanCheck):
    """[summary] StopPoint geocode is more than 100 metres from a road.


    Args:
        NaptanCheck ([type]): [description]
    """
    check_name = 'stop road distance.'
    check_geographic_level = 'stops'
    check_warning_level = 'high'

    @classmethod
    @NotImplementedError
    def stop_road_distance(cls, gdf):
        """[summary] 

            Args:
                gdf ([type]): [description]

            Raises:
                NotImplementedError: [description]

            Returns:
                [type]: [description]
            """
        check_name = "stop_road_distance".__name__
        # list of stops not in correct admin areas by geo position.
        failed_nodes = ''
        rep.report_failing_nodes(gdf, check_name, failed_nodes)
        return failed_nodes

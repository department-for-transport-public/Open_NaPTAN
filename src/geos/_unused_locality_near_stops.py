from report import reporting as rep
from cons._check_nodes_match_nptg import check_nodes_match_nptg_data

# from geos.stop_proximity import stop_proximity
from checks import NaptanCheck

# %%


class UnusedLocalities(NaptanCheck):
    """[summary] Locality has no stops or child Localities, but is within
    250 metres of a StopPoint associated with a different Locality.

    """

    check_name = "Unsuusedl locality near stops"
    check_warning_level = "medium"
    check_geographic_level = "locality"

    @classmethod
    @NotImplementedError
    def unused_locality_near_stops(cls, nodes, nptg):
        """[summary] Locality has no stops or child Localities, but is within
         250 metres of a StopPoint associated with a different Locality.


        Args:
            nodes ([type]): [description]
            nptg ([type]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        check_name = "unused_locality_near_stops"
        unused_localities = check_nodes_match_nptg_data(nodes, "")
        # list of unused localities, finding nearest naptan stop within the area.
        # geos.g
        # list of stops not in correct admin areas by geo position.

        failed_nodes = ""
        rep.report_failing_nodes(nodes, check_name, failed_nodes)
        return failed_nodes

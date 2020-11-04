from report import reporting as rep
from checks import NaptanCheck

# %%


class StopAdminGeoPosition(NaptanCheck):
    """[summary]

    Args:
        NaptanCheck ([type]): [description]
    """
    check_name = 'stops_in_different_admin_authority_geo_position'
    check_warning_level = 'high'
    check_geographic_level = 'stops'

    @classmethod
    def stops_in_different_admin_authority_geo_position(cls, gdf):
        """[summary] The AtcoCode prefix for the StopPoint represents an
        AdminArea other than the one associated with the stop‟s Locality.
        This test highlights those stops which are associated with a locality that
        is itself not in the same administrative area. This is often not wrong – 
        but in some cases it indicates a stop that is incorrectly located, or 
        associated with the wrong locality.

        Check each example and confirm that each represents a stop close to the
        boundary of your authority‟s area – and consider whether the locality
        association with each stop is reasonable, even if it is with a locality
        that is in the adjacent admin area. Check that the coordinates of the stop
        are right, and correct them if not. 
        Args:
            gdf ([gdf]): [the naptan total dataframe]
            stops ([node_type_stops]): [description]
            authorities ([gdf]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        check_name = "stops_in_different_admin_authority_geo_position"
        # TODO - check if any other stops or points are within the authority
        # TODO polygon of this boundary,
        # TODO check from the surrounding admin areas
        # TODO if so add the stop to the failed nodes report file
        # TODO include how the name of the other area and distance outside.
        #
        # list of stops not in correct admin areas by geo position.
        failed_nodes = ''
        rep.report_failing_nodes(gdf, check_name, failed_nodes)
        return failed_nodes
        raise NotImplementedError

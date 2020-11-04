from checks import NaptanCheck
from report import reporting as rep

# %%


class HailRideValidity(NaptanCheck):
    """[summary] 	Hail and Ride Bus Stops that do not have a valid entry,
     centroid or exit records.

    Args:
        NaptanCheck ([type]): [description]
    """
    check_name = "hail and ride is invalid."
    check_warning_level = 'high'
    check_geographic_level = 'stop areas'

    @classmethod
    @NotImplementedError
    def hail_ride_invalid(cls, gdf):
        """[summary] Hail and Ride Bus Stops that do not have a valid entry,
           centroid or exit record.

            Args:
                gdf([type]): [description]

            Raises:
                NotImplementedError: [description]

            Returns:
                [type]: [description]
            """
        check_name = "hail_ride_invalid"
        # list of stops not in correct admin areas by geo position.
        failed_nodes = ''
        rep.report_failing_nodes(gdf, check_name, failed_nodes)
        return failed_nodes

    @classmethod
    @NotImplementedError
    def hail_ride_section_length(cls, gdf):
        """[summary] Hail and Ride Bus Stop where total length of section is greater than 1km


        Args:
            gdf ([type]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        check_name = "hail_ride_section_length"
        # list of stops not in correct admin areas by geo position.
        failed_nodes = ''
        rep.report_failing_nodes(gdf, check_name, failed_nodes)
        return failed_nodes

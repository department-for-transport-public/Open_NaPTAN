from checks import NaptanCheck

# %%


class StopProximity(NaptanCheck):
    """[summary] Stop is too close to another stop. Any stops within 4 metres of another stop will flag as a warning.
        For stops of type BCS this threshold is reduced to 2 metres.
        Only stops of type BCT, BCS and BCQ are included in this test.

    Args:
        NaptanCheck ([type]): [description]
    """

    check_name = "Stop proximity"
    check_geographic_level = ["stops", "locality"]
    check_warning_level = "high"

    @classmethod
    def stop_proximity_street_side(cls, gdf):
        """Descriptions: Stop is too close to another stop, any stop within 4
        meters of another stop will flag as a warning. BCS type the threshold
         is 2 meters.

           Args:

           Returns:
        """
        # filter by the require stop type,
        busstops = NaptanCheck.filter_bus_stops(gdf, bus_stop_types=["BCT", "BCQ"])
        # check the distance
        return busstops
        #

    @classmethod
    def stop_proximity_coach_bay(cls, gdf):
        """[summary]

        Args:
            gdf ([type]): [description]
        """
        # filter by the require stop type,
        busstops = NaptanCheck.filter_bus_stops(
            gdf, bus_stop_types=["BCS", "BCT", "BCQ"]
        )
        return busstops

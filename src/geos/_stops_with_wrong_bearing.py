from checks import NaptanCheck

# %%


class StopsBearing(NaptanCheck):
    """[summary] top has a bearing that is different to the calculated bearing
        of the road link it is connected to.
        The test compensates for stops being snapped to the wrong side of the road.
        Therefore if the calculated bearing is E then stops with a bearing of E or W
        will be allowed.
        A 22.5 degree boundary threshold is also allowed. Therefore for example if the
        calculated bearing in degrees is 280 (which falls in the range for W), as this
        falls within 22.5 degrees of the boundary to NW (292.5 degrees) allowed
        values will be W, NW and the mirror values of E, SE.

    Args:
        NaptanCheck ([type]): [description]
    """
    check_geographic_level = 'stops'
    check_name = 'stops with wrong bearing'
    check_warning_level = 'medium'

    @classmethod
    def stops_with_wrong_bearing(cls, gdf):
        """ Descriptions: The bearing shown in the data does not correspond with
            the bearing as calculated by reference to the orientation of the road
            at the location of the stopping point. Note this is not the direction
            of the road or the direction of travel the bus is taking necessarily.
            This is the way the bus is facing when it is stationary, picking/
            dropping passengers

            Args:

            Returns:
        """
        pass

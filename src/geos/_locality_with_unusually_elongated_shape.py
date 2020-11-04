from report import reporting as rep
from checks import NaptanCheck
from geos.CheckLocalPolygons import PolygonStructure


# %%


class UnusallyElongatedShape(NaptanCheck):
    """[summary]

    Args:
        NaptanCheck ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """

    check_name = "Locality_Size is unusually elongated in length."
    check_warning_level = "high"
    check_geographic_level = "locality"

    @classmethod
    @NotImplementedError
    def locality_with_unusually_elongated_shape(cls, gdf_locality):
        """[summary] the enclosing bounding box is arbitrary - this check
        and all other checks that require to build a shape are variants of
        Minimum Bounding Box/Convex Hull problems
        (https://en.wikipedia.org/wiki/Minimum_bounding_box_algorithms). There
        should be something pre-made in python, otherwise we can just look at
        implementing an existing algorithm. Many of these problems are
        arbitrarily defined by ITO, so we need to come up with a definition
        of "elongated" (assuming it is really a problem). For example, we could
        say that the shape is elongated if the longest edge is 10x longer than
        the shortest edge. We need to think what makes sense.

        Args:
            gdf ([type]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        check_name = "locality_with_unusually_elongated_shape"

        PolygonStructure.check_area_length_is_regular(gdf_locality, "Name of locality")
        # list of stops not in correct admin areas by geo position.
        # TODO - if
        failed_nodes = ""

        rep.report_failing_nodes(gdf_locality, check_name, failed_nodes)
        return failed_nodes
        raise NotImplementedError

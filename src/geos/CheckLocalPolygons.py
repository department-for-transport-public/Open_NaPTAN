# %%
import etl.etl_pipe
from etl.etl_pipe import create_naptan_subframe as cns
import sys
from shapely.geometry import Point, Polygon, LineString, LinearRing
from checks import NaptanCheck
from etl.geo_pipe import make_naptan_polygon
import pyproj
from functools import partial
from shapely.ops import transform
from report import reporting as rep
import numpy as np

# %%


class PolygonStructure(NaptanCheck):
    """[summary] a collection of methods for checking that locality level
    polygons are the correct size.
    Required for checking that the hail and ride section length is not over a 1km.
    Logic test for checking the length of localities are logic and no boundary
    point is more than 10x the distance from shortest distance boundary point.
    Args:
        NaptanCheck ([type]): [description]

    Raises:
        ve: [description]
        e: [description]

    Returns:
        [type]: [description]
    """

    # for reporting
    check_name = "Check Polygon Structure"
    check_warning_level = "medium"
    check_geographic_level = "Locality"

    @classmethod
    def polygon_longest_side(cls, locality_polygon):
        """[summary] Get the longest side of a given polygon, in meters, if it
        is over 10x time the length of the shortest side, this raises a medium
        level warning as the locality is likely including nodes that are not
        correct.

        Arguments:
            polygon {[shapely.geometry.polygon.Polygon]} -- [the polygon of the
            given area, ]

        Raises:
            NotImplemented: [description]

        Returns:
            [type] -- [description]
        """

        check_name = "Check Polygon length is not too long."
        polygon = locality_polygon
        try:
            # get minimum bounding box around polygon
            box = polygon.minimum_rotated_rectangle
            # get coordinates of polygon vertices
            x, y = box.exterior.coords.xy
            # get length of bounding box longest edge
            edge = (
                Point(x[0], y[0]).distance(Point(x[1], y[1])),
                Point(x[1], y[1]).distance(Point(x[2], y[2])),
            )
            # get length of polygon as the longest edge of the bounding box
            longest_length = max(edge)
            # returns the longest length
            return longest_length
        except ValueError as ve:
            raise ve
        except AttributeError as ae:
            raise ae
        except Exception as e:
            raise e

    @classmethod
    def polygon_shortest_side(cls, locality_polygon):
        """[summary] Check that the shortest side is not under 4 meters, as that
        would indicated that naptan nodes are too close together.

        Args:
            polygon ([type]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """

        check_name = "Check polygon shortest side is not too short."
        polygon = locality_polygon

        try:
            # get minimum bounding box around polygon
            box = polygon.minimum_rotated_rectangle
            # get coordinates of polygon vertices
            x, y = box.exterior.coords.xy
            # get length of bounding box longest edge
            edge = (
                Point(x[0], y[0]).distance(Point(x[1], y[1])),
                Point(x[1], y[1]).distance(Point(x[2], y[2])),
            )
            # get length of polygon as the longest edge of the bounding box
            shortest_length = min(edge)
            # returns the shortest length
            return shortest_length
        except Exception as e:
            sys.exit(f"{check_name} has failed due to {e}.")

    @classmethod
    def check_polygon_length(cls, gdf, locality_name):
        """[summary] if a polygon side length is more than 10x the length of
        the shortest side then the polygon is likely the incorrect length

        Args:
            locality_name ([type]): [description]
            locality_length ([type]): [description]

        Returns:
            [type]: [description]
        """
        # TODO, make a naptan subframe for the locality.
        # TODO make a polygon based off of naptan data

        # TODO compare the two lengths

        return result

    @classmethod
    def check_area_length_is_regular(cls, gdf, naptan_locality):
        """[summary] when given a geodataframe, checks the matching polygon, is
        under a 1000 nodes

        Args:
            gdf ([naptan master geodataframe]): [the naptan master.]
            df_area ([naptan geodataframe]): [the sub area we are checking,
            not we pass the entire frame, (a locality)]
            polygon ([[shapely.geometry.polygon.Polygon]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        check_name = cls.check_area_length_is_regular.__name__
        # make the polygon from area data, cehck length
        area_polygon = make_naptan_polygon(naptan_locality)
        # TODO get the longest length
        poly_long = cls.polygon_longest_side(area_polygon)
        # TODO get the shortest length
        poly_short = cls.polygon_shortest_side(area_polygon)
        # check area length.
        if poly_long >= 800:
            print("Is not a locality and the area is excluded from this check")
            pass
        elif poly_long <= 1000:
            print("Polygon area is regular")
        else:
            print("Polygon area is irregular")
            rep.report_failing_nodes(gdf, check_name, naptan_locality)

    @classmethod
    def locality_naptan_projected_square_area(cls, naptan_locality):
        """[summary] use proj to create a sq area base off of the naptan
         locality

        Args:
            naptan_locality ([type]): [description]
        """

        # make a polygon of the naptan area.
        local_poly = make_naptan_polygon(naptan_locality)
        # transform the geometry points into a sq meter area result.
        geom_area = transform(
            partial(
                pyproj.transform,
                # the result as a spheroid
                pyproj.Proj(init="EPSG:4326"),
                pyproj.Proj(
                    proj="aea", lat_1=local_poly.bounds[1], lat_2=local_poly.bounds[3]
                ),
            ),
            local_poly,
        )
        print(f"Locality area is {geom_area.area}m^2")
        return geom_area.area
        # Output in m^2: 1083461.9234313113

    @classmethod
    @NotImplementedError
    def check_naptan_locality_area_size(cls, locality_name, locality_projected_size):
        """[summary]

        Args:
            locality_projected_size ([type]): [description]

        Returns:
            [type]: [description]
        """
        # TODO -> check the area size is below a set amount.
        # TODO determine the very generous limit of a locality size.
        locality_limit = ""
        if locality_projected_size <= locality_limit:
            print(f"{locality_name} sq area limit is acceptable size.")
        else:
            # TODO report error of limit.
            result = ""
            return result

    @classmethod
    def find_further_point(cls, polygon, x, y, bearing):
        """[summary]

        Args:
            polygon ([type]): [description]
            x ([type]): [description]
            y ([type]): [description]
            bearing ([type]): [description]
        """
        # get the 4 cardinal boundaries.
        east, south, west, north = polygon.bounds
        # get the absolute line length of oppositionals
        line_length = max(abs(east - west), abs(north - south)) * 2
        # np.sin of the gradiant bearing.
        new_x = x + (np.sin(np.deg2rad(bearing)) * line_length)
        # cos sin of the gradiant bearing line.
        new_y = y + (np.cos(np.deg2rad(bearing)) * line_length)
        # line string object
        l = LineString([[x, y], [new_x, new_y]])
        # linear ring coordinates
        lr = LinearRing(polygon.exterior.coords)
        # measure intersection of the linear ring with the line,
        intersections = lr.intersection(l)

        return intersections.x, intersections.y


# %%
lambeth = cns(gdf, "LocalityName", "lambeth")
locality_area_size = PolygonStructure.locality_naptan_projected_square_area(lambeth)
PolygonStructure.check_naptan_locality_area_size(locality_area_size)

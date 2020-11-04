import pandas as pd
from report import reporting as rep

from checks import NaptanCheck

# %%


class MultiRoadName(NaptanCheck):
    """[summary] A collection of methods to check that the roads names contain
    the correct types and collection of words.

    Args:
        NaptanCheck ([type]): [description]

    Returns:
        [type]: [description]
    """

    # for reporting
    check_name = "Check Multiroad Name words in stop"
    check_warning_level = "low"
    check_geographic_level = "stops"

    @classmethod
    def stop_with_multiple_road_names(cls, gdf, col_name="CommonName"):
        """[summary]CommonNames in NaPTAN should be simple and not composite.
            Most examples of commonnames which include two of the designated
            words are ones where two road names are used in a composite name,
            contrary to NaPTAN guidance.
            This uses regex, but they could be some other way of doing this...
        Arguments:
            df {[type]} -- [description]
        """
        swmrn_gdf = gdf
        swmrn_gdf[col_name] = swmrn_gdf[col_name].str.lower()
        try:
            # leave this here, no it's not being used, just leave it anyway.
            targets = [
                "road",
                "roads",
                "street",
                "streets",
                "avenue",
                "avenues",
                "garden",
                "gardens",
                "lane",
                "lanes",
                "drive",
                "drives",
                "way",
                "ways",
            ]

            # regex patterns for detection.
            pattern = r"\b(road|roads|\
                            street|streets|\
                            avenue|\avenues|\
                            garden|gardens|\
                            lane|lanes\
                            drive|drives\
                            way|ways)\b"

            fail_rds_re = (
                r"\b('street|streets|avenue|avenues|garden|"
                r"gardens|lane|lanes|drive|drives|way|ways')\b"
            )
            fail_aves_re = (
                r"\b('road|roads|street|streets|garden|gardens|"
                r"lane|lanes|drive|drives|way|ways')\b"
            )
            fail_gdns_re = (
                r"\b('road|roads|street|streets|avenue|avenues|"
                r"lane|lanes|drive|drives|way|ways')\b"
            )
            fail_lanes_re = (
                r"\b('road|roads|street|streets|avenue|avenues|"
                r"garden|gardens|drive|drives|way|ways')\b"
            )
            fail_drives_re = (
                r"\b('road|roads|street|streets|avenue|avenues|"
                r"garden|gardens|lane|lanes|way|ways')\b"
            )
            fail_ways_re = (
                r"\b('road|roads|street|streets|avenue|avenues|"
                r"garden|gardens|lane|lanes|drive|drives')\b"
            )

            tn = swmrn_gdf[swmrn_gdf[col_name].str.contains(pattern, regex=True)]
            roads = tn[tn[col_name].str.contains(r"\b(road|roads)\b")]
            fail_rds = roads[roads[col_name].str.contains(fail_rds_re, regex=True)]
            aves = tn[tn[col_name].str.contains(r"\b(avenue|avenues)\b")]
            fail_aves = aves[aves[col_name].str.contains(fail_aves_re, regex=True)]
            gdns = tn[tn[col_name].str.contains(r"\b(garden|gardens)\b")]
            failgdns = gdns[gdns[col_name].str.contains(fail_gdns_re, regex=True)]
            lanes = tn[tn[col_name].str.contains(r"\b(lane|lanes)\b")]
            faillanes = lanes[lanes[col_name].str.contains(fail_lanes_re, regex=True)]
            drives = tn[tn[col_name].str.contains(r"\b(drive|drives)\b")]
            faildrives = drives[
                drives[col_name].str.contains(fail_drives_re, regex=True)
            ]
            ways = tn[tn[col_name].str.contains(r"\b(way|ways)\b")]
            failways = ways[ways[col_name].str.contains(fail_ways_re, regex=True)]
            all_dfs = [fail_rds, fail_aves, failgdns, faillanes, faildrives, failways]
            failed_nodes = pd.concat(all_dfs)
            failed_nodes[col_name] = failed_nodes[col_name].str.title()
            rep.report_failing_nodes(
                gdf, "Stop with Multiple road type names", failed_nodes
            )
            return failed_nodes
        except Exception as e:
            raise (e)

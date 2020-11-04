from checks import NaptanCheck
from report import reporting as rep
from global_land_mask import globe


# %%


class CoastlineStops(NaptanCheck):
    """[summary] StopPoint geocode is more than 50 metres away from land.

    Args:
        NaptanCheck ([type]): [description]
    """
    check_geographic_level = 'stops'
    check_name = 'StopPoint is more than 50 metres away from land.'
    check_warning_level = 'high'

    @classmethod
    def naptan_coastal_nodes(cls, gdf):
        # TODO - add a column to the master naptan dataframe, and then count up
        #  false values, to get the percent of stops that fail, and then compare
        #  those stops, to find out which ones are near the coast and how near
        #  the coast they are.
        """[summary] provided a dataframe, returns a list of nodes that are near the
            coast line, this uses global land mask library, a numpy & pandas extension,
            for mapping the boundaries of the coastline.

            Arguments:
                df {[geospatial dataframe]} -- [the naptan master dataframe.]

            Raises:
                ve: [Raises description]
                e:  []
            Returns:
                [type] -- [description]
            """

        check_name = "naptan_coastal_nodes"
        try:
            # remove ferry based stops / jetty stop types, as they proximity to the
            # coastline isn't a problem.
            coastal_infrastructure = ['FTD', 'FBT', 'FER']
            gdf = gdf[~gdf['StopType'].isin(coastal_infrastructure)]
            # we compare against the compressed land geometry dataset for
            # coordinates outside the coastline.
            gdf['Land_State'] = globe.is_land(gdf['Latitude'],
                                              gdf['Longitude'])
            coastal_nodes = gdf.loc[~gdf.Land_State]
            # get the count of failing nodes as a values
            high_node_areas = coastal_nodes['LocalityName'].value_counts()
            percent = ((len(coastal_nodes) / len(gdf)) * 100.0)
            # if the number of nodes is over this percent, console warning.
            if percent >= 1.1:
                print(
                    f"The {gdf.AreaName.iloc[0]} has {len(coastal_nodes)} stops\
                    that are off the UK Coastline, that is {percent: 0.2f} %\
                    of all stops in the named admin area.")
            elif percent <= 0:
                print('No Nodes were found along the coastline.')
                pass
            else:
                print(
                    f"The area has {len(coastal_nodes)} nodes that are off the\
                      coastline boundary. UK coastline, this is {percent: 0.2f} % of all nodes in the area.")
            rep.report_failing_nodes(gdf, check_name, coastal_nodes)
            return high_node_areas

        except ValueError as ve:
            raise(ve)

        except Exception as e:
            print(e)

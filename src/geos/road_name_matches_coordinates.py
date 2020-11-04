from report import reporting as rep
import etl.geo_pipe as geopipe


# %%
def road_name_matches_coordinates(gdf, atcocode):
    """[summary] Checks that the road name in the record, matches if the
       The “street” shown in the data does not correspond with the name
       attached to the road segment to which the stop is snapped in the Navteq
       mapping data used by Ito.
    Arguments:
        gdf {[geopandas dataframe]} -- [pass in the chosen dataframe]
        ATCOCode {[str]} -- [Pass in the given naptan unique stop id.]

    Returns:
        [type] -- [description]
    """
    # check name
    check_name = road_name_matches_coordinates.__name__
    # masking ideally.
    gdf1 = gdf
    node = gdf1.loc[gdf1['ATCOCode'] == atcocode]
    # api call to get nearest road name
    found_name = geopipe.get_nearest_road_name(gdf1, atcocode)
    if found_name[1] == node['Street'][0]:
        print('Road Name Matches')
        pass
    else:
        # TODO - needs testing.
        res = node["ATCOCode"]
        rep.report_failing_nodes(gdf, check_name, res)
        return res

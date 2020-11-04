from checks import NaptanCheck
from etl import geo_pipe, etl_pipe
from report import reporting as rep


# %%
class LocalityStructureCheck(NaptanCheck):
    """[summary] Checks to be conducted on the locality data structure generated
    by Naptan and where naptan localities interface with nptg localities.

    Args:
        NaptanCheck ([type]): [description]
    """
    check_warning_level = 'high'
    check_geographic_level = 'locality'
    check_name = 'Locality not unique nationally.'

    @classmethod
    def locality_not_unique(cls, gdf):
        """[summary] The name of the locality with its qualifier (if any) is not
        unique nationally. To ensure that a search for a locality based on the
        National Gazetteer (NPTG) will differentiate between localities that
        may be identically named, by applying an appropriate qualifier to each
        ambiguous entry. Ensure that the appropriate qualifier is added to a
         locality which is ambiguous.

        Args:
            gdf ([type]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        check_name = "locality_not_unique"
        gdf['Local_Qualifer_Name'] = gdf['LocalityName'] + \
            ', ' + gdf['QualifierName']
        # remove all the notana values from the dataframe.
        nodes = gdf[gdf["Local_Qualifer_Name"].notna()]
        # check for duplicates in the locality qualifier name column.
        boolean = nodes.duplicated(subset=['Local_Qualifer_Name'])
        nodes_dup = nodes[boolean]
        # TODO this might work, it returns 8000 localities out of 28000 that are
        # not unique... not sure that all is correct.
        a = nodes_dup.loc[~nodes_dup.duplicated(keep=False),
                          'Locality_Qualifier_Name'].unique()
        # TODO check that the returned are correct

        failed_nodes = ''
        rep.report_failing_nodes(gdf, check_name, failed_nodes)
        return failed_nodes
        raise NotImplementedError

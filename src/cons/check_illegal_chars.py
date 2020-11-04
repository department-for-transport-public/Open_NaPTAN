import regex as re
from report.reporting import report_failing_nodes

from checks import NaptanCheck

# %%


class IllegalCharacters(NaptanCheck):
    """[summary] 	StopPoint has a CommonName that contains one of the
    following illegal characters: ?, !, [, ], ., ,, /, and (, ) for stop
    types BCT and BCS.
    Exceptions: NO., O/S, P.H., P.O., ST. (case-insensitive).

    Args:
        NaptanCheck ([type]): [description]

    Returns:
        [type]: [description]
    """

    # for reporting
    check_name = 'Check Illegal Characters'
    check_warning_level = 'low'
    check_geographic_level = 'stop'

    @classmethod
    def check_illegal_characters(cls, gdf, col_name='StopPoint'):
        """[summary - removes illlegal characters from the given Naptan stops file.

        Arguments:
            gdf {[geopandas dataframe]} -- [the naptan master dataframe]
            columnName {[str]} -- [a given column name to search through]
        Returns:
            df -- a df object that consists of only stops with illegal
             characters removed, from the
            given field.
        """
        check_name = 'Check Illegal Characters'
        # our regex pattern of allowed special characters in stop point names
        pattern = r"\bO/S|NO\.|P\.H\.|P\.O\.|ST\.|'s|St\.|st.\b"
        # our none allowed non-alphanumeric characters.
        searchfor = ['!', '[', ']', '.', ',', '/', '/?']
        # clone dataframe, removing none
        gdf1 = IllegalCharacters.filter_bus_stops(gdf)
        # remove the nodes with the permitted exceptions.
        excluded_nodes = gdf1[gdf1[col_name].str.contains(pattern,
                                                          case=False,
                                                          regex=True)]
        mask = gdf1[col_name].isin(excluded_nodes[col_name])
        # removing excluded nodes from bus stops frame.
        gdf_filter = gdf1[~mask]
        # use map and regex to create a generator that str contain
        pat = '|'.join(map(re.escape, searchfor))
        # check the given column for any illegal characters
        filtered_nodes = gdf_filter[gdf_filter[col_name].str.contains(pat)]
        # report on failing nodes that contain illegal characters.
        report_failing_nodes(gdf,
                             check_name,
                             filtered_nodes)
        return filtered_nodes

import sys
from checks import NaptanCheck
import pandas as pd
import numpy as np
from etl import etl_pipe
from report import reporting as rep
from visualise.visualiser import generate_base_map


# %%
class StopNameLexicalStructure(NaptanCheck):
    """[summary] StopPoint has a full name [Locality, CommonName (Indicator)]
     containing three or more occurrences of any single word.


    Args:
        NaptanCheck ([type]): [description]
    """
    check_name = 'stop name with repeating words in the stop point.'
    check_geographic_level = 'stops'
    check_warning_level = 'low'

    @classmethod
    def node_repeating_word(cls, df):
        """[summary] StopPoint has a full name [Locality, CommonName (Indicator)]
        containing three or more occurrences of any single word.
        There is a standard minimum content for the unique identification of stops
        in downstream systems – which comprises “Locality (without qualifier),
        Common Name (indicator)”.
        Downstream systems using the data do not want unnecessary duplication of
        words within this formulation of stop names (on timetables, for instance)
        this test identifies situations in which the same word appears three or
        more times in the concatenated stopname.

        Arguments:
            df {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        check_name = "Node_Has_Repeating_Word".__name__
        df1 = df[['ATCOCode', 'CommonName', 'LocalityName', 'Indicator']]
        spec_chars = ["!", '"', "#", "%", "&", "'", "(", ")",
                      "*", "+", ",", "-", ".", "/", ":", ";", "<",
                      "=", ">", "?", "@", "[", "\\", "]", "^", "_",
                      "`", "{", "|", "}", "~", "–"]
        for char in spec_chars:
            df1['CommonName'] = df1['CommonName'].str.replace(char, ' ')
        split = df1['CommonName'].str.split(expand=True)
        split1 = df1['LocalityName'].str.split(expand=True)
        split2 = df1['Indicator'].str.split(expand=True)
        df2 = pd.concat([split, split1, split2],
                        axis=1,
                        ignore_index=True)

        df3 = (df2.fillna('')
               .groupby(df2.columns.tolist()).apply(len)
               .rename('Repeat_Count')
               .replace('', np.nan)
               .sort_values(by=['Repeat_Count'], ascending=False))
        # TODO this works but can't be assigned,
        mask = (df3['Repeat_Count'] > 2)
        # back to the original data frame for boolean indexing
        return mask
        raise NotImplementedError
        print('Not implemented at this time.')

    # %%
    @classmethod
    def node_has_repeating_word(cls, gdf):
        """[summary]

        Raises:
            NotImplementedError: [description]
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        check_name = "node_has_repeating_word".__name__
        gdf1 = gdf[['ATCOCode',
                    'CommonName',
                    'LocalityName',
                    'Indicator']].apply(lambda x: ' '.join(x.astype(str)),
                                        axis=1)
        split = gdf1['CommonName'].str.split(expand=True)
        split1 = gdf1['LocalityName'].str.split(expand=True)
        split2 = gdf1['Indicator'].str.split(expand=True)
        gdf2 = pd.concat([split, split1, split2],
                         axis=1,
                         ignore_index=True)
        raise NotImplementedError

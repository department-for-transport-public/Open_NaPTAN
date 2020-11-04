import sys
from report import reporting as rep
from checks import NaptanCheck

# %%


class IllegalSpaces(NaptanCheck):
    """[summary] A collection of methods for handling the presence of the
    illegal spaces in the naptan dataset.

    Args:
        NaptanCheck ([type]): [description]
    """

    # for reporting
    check_name = "Check Illegal spaces"
    check_warning_level = "low"
    check_geographic_level = "stop"

    def old_check_illegal_spaces(cls, gdf, col_name):
        """[summary]

        Args:
            gdf ([geopandas]): [the naptan geodataframe]
            col_name ([str]): []

        Returns:
            [type]: [description]
        """
        # the column will sometimes misread as containing floats.
        gdf[col_name] = gdf[col_name].astype(str).str.replace("\\D+", "")
        # strip leading and trialing space
        gdf[col_name] = gdf[col_name].apply(lambda x: x.strip())
        # remove white space between strings
        gdf[col_name] = gdf[col_name].replace("\\s+", " ", regex=True)
        # cast to the result.
        ris_gdf = gdf
        return ris_gdf
        # if we fix the columns, we don't need to report them,
        #  currently.

    @classmethod
    def check_illegal_spaces(cls, gdf):
        """[summary]
        Removes any and all extra spaces they may have been added
        by accident to a naptan field, in the commonname, indicator, street,
        landmark, town, suburb, locality. As we are cleaning data we don't want
        to report back. report on all the affected columns for this test.

        Arguments:
            gdf {[geopandas dataframe]} -- [a pandas dataframe with extra
            spaces involved.]

        Returns:
            [geopandas dataframe] -- [a naptan dataframe with extra spaces
            removed.]
        """
        #
        check_name = "Check Illegal Spaces"
        #
        cols = [
            "CommonName",
            "LocalityName",
            "Indicator",
            "Street",
            "Landmark",
            "Town",
            "Suburb",
        ]
        # TODO this should be able to be applied to you.
        try:
            for colname in cols:
                # the column will sometimes misread as containing floats.
                gdf[colname] = gdf[colname].astype(str).str.replace("\\D+", "")
                # strip leading and trialing space
                gdf[colname] = gdf[colname].apply(lambda x: x.strip())
                # replace any number of blank spaces with a single space.
                gdf[colname] = gdf[colname].str.replace(" +", " ")
                # cast results to a new dataframe
                gdf_cleaned = gdf
        except Exception as e:
            print(f"{check_name} has failed due to {e}.")
            pass
        finally:
            #  report the failing dataframes.
            rep.report_failing_nodes(gdf, check_name, gdf_cleaned)
            print(f"{check_name}, has been completed.")

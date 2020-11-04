import sys
from report import reporting as rep
from checks import NaptanCheck

# %%


class AtcocodeCheck(NaptanCheck):
    """[summary] A collection of methods to check the integrity of the atcocode
    code structures used to identify.

    Args:
        NaptanCheck ([type]): [description]

    Returns:
        [type]: [description]
    """

    # for reporting
    check_name = "Check Illegal Characters"
    check_warning_level = "low"
    check_geographic_level = "stop"

    @classmethod
    def check_atcocode_length(cls, gdf):
        """[summary] checks the atcocode (unique identifier) length is 12 and if
        not the stop fails the check.

        Args:
            gdf ([geopandas dataset, master or sub]): [description]

        Returns:
            [geopandas dataframe]: [Geopandas dataframe of failed nodes.]
        """
        #  variance? Stop type? Authority?
        check_name = "check_atcocode_length_is_12"
        gdf["AtcoCode_Character_Len"] = gdf["ATCOCode"].apply(len)
        fail_range = gdf["AtcoCode_Character_Len"].unique()

        try:
            # create a mask that include no inactive nodes and atcocodes under
            # 12
            if len(fail_range) != 1:
                mask = (gdf["Status"] != "del") & (gdf["AtcoCode_Character_Len"] != 12)
                # get the failing nodes.
                fn = gdf[mask]
                # makes report
                rep.report_failing_nodes(gdf, check_name, fn)
                # TODO make a sample level map of the failing area with codes.
                # get the name of the area that is failing
                fail_area = gdf.AreaName.iloc[0]
                print(fail_area)
                # the below returns a short dataframe counting the number of
                # atcocodes.
                # that are less than 12 alphanumeric characters in length.
                result_agg = (
                    fn[["AtcoCode_Character_Len", "ATCOCode"]]
                    .groupby(["AtcoCode_Character_Len"])
                    .count()
                )

                return result_agg

        except ValueError as ve:
            sys.exit(f"This error occured {ve}")
        except Exception as e:
            sys.exit(f"{e} was encounter check has been cancelled.")
        else:
            message = f"{gdf.AreaName.iloc[0]} all Atcocode unique identifiers are the correct length."
            rep.write_basic_log_file(message)

    @classmethod
    @NotImplementedError
    def check_atcocode_format(cls, gdf):
        """[summary] check that Atcocode format is not correct, the format should
        start with the 3 digit area code, then either 0 if a lone stop or 'g'
         if part of a stop group.

        Args:
            gdf ([type]): [description]
        """

        #  TODO - check that atcocodes are the correct format.

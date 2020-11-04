import sys
import pandas as pd
import numpy as np
from report import reporting as rep
from src.checks import NaptanCheck

# %%


class NameContainsLocality(NaptanCheck):
    """[summary]

    Args:
        NaptanCheck ([type]): [description]
    """

    # for reporting
    check_name = "Stop Name contains locality name."
    check_warning_level = "medium"
    check_geographic_level = "stop"

    @classmethod
    def stop_name_contains_locality_name(cls, gdf):
        """[summary]- When stop names are presented in public information systems
            they are generally shown with the locality. If the CommonName also
            includes the name of the locality, then the result is duplication
            in the concatenated stopname, which makes the name longer than is
            necessary. However, there are situations where the name of the stop
            legitimately will include the locality name – such as
            “Rugby School” – because “Rugby, School” could refer to any one of
            many schools, only one of which is “Rugby School”.

        Arguments:
            gdf {[geopandas dataframe]} -- [the naptan master dataframe]

        Returns:
            [geopanads dataframe] -- [a list of all stops where the common name and
            locality name, match exactly and no excluding terms are found to excuse
            this, there should be a set number of them but if that number
            increases, this should be addressed.]
        """

        check_name = "Stop Name contains locality name."
        try:
            df = gdf[["ATCOCode", "CommonName", "LocalityName"]]
            cn, ln = df["CommonName"], df["LocalityName"]
            cnsum, lnsum = cn.isnull().sum(), ln.isnull().sum()
            # permitted terms to include
            terms = [
                "Academy",
                "Arms",
                "Avenue",
                "Bridge",
                "Centre",
                "Church",
                "Close",
                "Club House",
                "College",
                "Common",
                "Corner",
                "Cottages",
                "Crescent",
                "Cross Roads",
                "Cross",
                "Crossroads",
                "Dock",
                "Drive",
                "Estate",
                "Farm",
                "Ferry",
                "Gardens",
                "Green",
                "Hall",
                "Health Centre",
                "Hill",
                "Hospital",
                "Hotel",
                "House",
                "Hoverport",
                "Industrial Area",
                "Inn",
                "Island",
                "Junction",
                "Landing",
                "Lane",
                "Lodge",
                "Main Street",
                "Manor",
                "Metrolink",
                "Mill",
                "Park",
                "Pier",
                "Place",
                "Post Office",
                "Rail",
                "Railway",
                "Rd",
                "Road",
                "Roundabout",
                "School",
                "Square",
                "Station",
                "Street",
                "Supertram",
                "Terminal",
                "Terrace",
                "Tramlink",
                "Tramway",
                "Turn",
                "Underground",
                "Village",
                "Way",
            ]

            # combine the names into a zip
            df_combined = [
                df[0] in df[1] for df in zip(df["CommonName"], df["LocalityName"])
            ]
            # convert to a pandas column series
            colvalues = pd.Series(df_combined)
            # add to the existing dataframe
            df.insert(loc=0, column="NameMatch", value=colvalues)
            # check if the data frame is empty or not and the name match column contains values.
            if not df["NameMatch"].isnull().all():
                mns = df[df["NameMatch"]]
                #
                mns = mns.drop(["NameMatch"], axis=1)
                # we create a mask to identify an excluded terms occuring in
                # the remain duplicates, that should be ignored. We do this
                # for both the Common name and Localityname, column.
                cn_mask = np.logical_or.reduce(
                    [
                        mns["CommonName"].str.contains(t, regex=False, case=False)
                        for t in terms
                    ]
                )
                # return common name mask and added
                mns = mns[cn_mask]
                #
                ln_mask = np.logical_or.reduce(
                    [
                        mns["LocalityName"].str.contains(t, regex=False, case=False)
                        for t in terms
                    ]
                )
                #
                mns = mns[ln_mask]
                # reports returns percentage of bad stops out of all stsops,
                # about 0.03%
                rep.report_failing_nodes(gdf, check_name, mns)
                return mns
            # double check if the return data frame is empty or not, if it's empty, we are good for that area.
            elif df["NameMatch"].isnull().all():
                success_message = f"{gdf.AreaName.iloc[0]} has no stops names containing locality names."
                rep.write_basic_log_file(success_message)

        except ValueError as ve:
            # ValueError: Cannot mask with non-boolean array containing NA /
            #  NaN values
            raise ve
            sys.exit(f"{check_name} failed because of {ve}")

import sys
from report import reporting as rep
from src.checks import NaptanCheck

# %%


class StopNameHighRisks(NaptanCheck):
    """[summary]

    Args:
        NaptanCheck ([type]): [description]
    """
    # for reporting
    check_name = 'Stop Name contains high risk words.'
    check_warning_level = 'low'
    check_geographic_level = 'stop'

    @classmethod
    def stop_names_with_high_risk_words(cls, gdf):
        """[summary] Descriptions: StopPoint has a CommonName that contains one of
        the following high risk words: DELETE, DELETED, N/A, N/K, OBSOLETE,
            UNUSED (case-insensitive).
        Args:
            gdf ([geopandas ]): [a pandas dataframe of the current naptan file.]

        Returns:
            df_risks [type]: [csv file containing risk updates.]
        """

        # name of check.
        check_name = "stop_names_with_high_risk_words"
        # clone
        gdf1 = gdf
        try:
            # list of risk words.
            riskwords = ['DELETE', 'DELETED', 'N/A', 'NOT IN USE'
                         'N/K', 'OBSOLETE', 'UNUSED']
            # text captialising managment
            gdf1['CommonName'] = gdf1['CommonName'].str.upper()
            gdf1['RiskWords'] = gdf1['CommonName'].apply(
                lambda x: 1 if any(i in x for i in riskwords) else 0)
            #
            df_risks = gdf1.loc[gdf1['RiskWords'] != 0]
            #
            endcol = len(df_risks.columns)
            #
            df_risks.insert(endcol, 'Warning Flag', check_name)
            #
            rep.report_failing_nodes(gdf, check_name, df_risks)
            return df_risks
            # TODO indicate if it's a bus stop, if so flag locality or
            # TODO authorities that should confirm the stops deletion from the
            # TODO database.
        except Exception as e:
            raise(e)
            sys.exit(f"{check_name} has failed due to {e}.")

import sys
from report import reporting as rep

from src.checks import NaptanCheck

# %%


class LocalitiesIDStops(NaptanCheck):
    """[summary] A collection of methods for handling localites with duplicate
    stop ids.

    Args:
        NaptanCheck ([type]): [description]
    """

    @classmethod
    def localities_with_identical_stops(cls, gdf_locality):
        """[summary]StopArea containing StopPoints that do not have identical
        CommonNames.

        The CommonName of stops within a single stoparea should be the same
        as each other (and the same as the name of the stoparea) wherever
        possible. This test identifies examples where the stopnames are not
        identical. At present this test does not identify cases where the stoparea
        name is different from any one or more of the individual stop‟s
        CommonName – but this may be added.

        Given a stop point within a locality, check if the stoppoint is duplicated
        at any point.

        Arguments:
            gdf {[geopandas dataframe]} -- [The Master naptan node frame.]

        Returns:
            df_warnings[type] -- [description]
        """
        # for reporting
        check_name = 'Check localities for identical stops.'
        check_warning_level = 'high'
        check_geographic_level = 'localities'
        # clone the stop name
        gdf1 = gdf_locality
        # get the area name.
        try:
            # check nptg locality length is not over 1, otherwise this is
            # not a single locality
            if len(gdf1['NptgLocalityCode'].unique()) == 1:
                # get duplicates.
                mask = gdf1['StopPoint'].duplicated()
                # mask
                failed_nodes = gdf1[mask]
                rep.report_failing_nodes(gdf_locality,
                                         check_name,
                                         failed_nodes)
                return failed_nodes

        except Exception as e:
            # pass if this is not a localities, we just catching.
            print(f'Not a locality, test can not be performed. {e}')
            pass

from checks import NaptanCheck
from etl import geo_pipe, etl_pipe
from report import reporting as rep

# %%


class DisusedLocalities(NaptanCheck):
    """[summary] Locality has no stops or child Localities, but is within 250
     metres of a StopPoint associated with a different Locality.


    Args:
        NaptanCheck ([type]): [description]
    """
    check_geographic_level = 'locality'
    check_name = 'unused localities near stops.'
    check_warning_level = 'medium'

    @classmethod
    def find_unused_localities(cls, gdf):
        """[summary] returns a list of admin areas in nptg,
            checks those are in the nodes file, if the nodes file has aac not in 

            Args:
                ([gdf])
            Raises:
                NotImplementedError: [description]
                ve: [description]

            Returns:
                [pandas.core.frame.DataFrame]: [localities that are not used in the
                nodes file.]
            """
        # node values

        localities = etl_pipe.naptan_gazette_localities()
        unused = localities[~localities['NptgLocalityCode'].isin(
            gdf['NptgLocalityCode'])]
        # converstion for geometry.
        unused = unused.rename(columns={"Gazette_Longitude": "Longitude",
                                        "Gazette_Latitude": "Latitude"})
        #
        unused = geo_pipe.calculate_naptan_geometry(unused)
        # reporting function
        rep.report_failing_nodes(
            gdf, 'unused localities near stops', failed_nodes=failedNodes)
        # m = vis.generate_base_map(unused, 'LocalityName')
        # m
        # TODO find out if any stops are inside the boundaries of the unused areas
        # TODO the geometries are just points for the unused localites
        # TODO find out the closest stops to these points.
        #  localites.
        return unused

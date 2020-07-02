import etl_pipeline as etl
import con_checks as con
import geo_checks as geo
import visualiser as vis
import click
import timeit


@click.command()
@click.option('--named_area',
              type=str, required=True,
              prompt='Enter an adminstrative area level name.',
              help='Provide the correct name from the administrative area list\
              .')
def main(named_area):
    """ Downloads the naptan dataset and runs the basic internal
     consistency checks and geospatial checks"""
    # etl pipeline functions.
    etl.downloads_naptan_data()
    etl.extract_naptan_files()
    naptanfilenames = etl.check_naptan_files()
    print(naptanfilenames)

    gdf = etl.read_naptan_file('stops')
    gdf = etl.calculate_naptan_geometry(gdf)
    gdf = etl.deactivated_nodes(gdf)
    # we join the gazette locality code and admin code data onto the nodes data
    # frame, this gives us accurate locality and admin area names.
    locality_codes = etl.naptan_gazette_localities()
    admin_codes = etl.naptan_gazette_admin_area_codes()
    gdf = etl.map_gazette_data_to_nodes(gdf,
                                        locality_codes,
                                        'NptgLocalityCode')
    gdf = etl.map_gazette_data_to_nodes(gdf,
                                        admin_codes,
                                        'AdminAreaCode')
    # we merge on the stop area data and corresponding codes for stop area
    gdf = etl.create_stop_areas(gdf)

    # cli to provide a named administrative area within the naptan dataset.
    # TODO or locality.
    naptan_area_level = 'AreaName'
    named_area = named_area
    gdf_sub = etl.create_naptan_subframe(gdf,
                                         naptan_area_level,
                                         named_area)

    # Data Cleansing functions #
    # illegal captials
    con.remove_illegal_caps(gdf_sub, 'StopPoint')
    #  illegal characters
    con.remove_illegal_chars(gdf_sub, 'StopPoint')
    con.remove_illegal_spaces(gdf_sub)
    print('Data cleansing completed.')

    # %% The internal data consistency checks
    con.check_name_too_long(gdf_sub)
    con.localities_with_identical_stops(gdf_sub)
    con.stop_name_contains_locality_name(gdf_sub)
    con.stop_with_bearing_missing(gdf_sub)
    con.stop_names_with_high_risk_words(gdf_sub)
    con.stops_in_different_admin_area(gdf_sub)
    print('All internal consistency checks have been completed.')

    # %% geospatial data checks
    geo.naptan_coastal_nodes(gdf_sub)
    etl.locality_level_checks(gdf_sub)
    # area specific checks
    print('All geospatial functions have been completed.')
    vis.visualise_stop_clusters(gdf_sub,
                                naptan_area_level,
                                named_area)


start = timeit.default_timer()
main('')
stop = timeit.default_timer()
exe_time = stop - start
print(f"Program Executed in {str(exe_time)}")

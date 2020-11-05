# %%
from etl import etl_pipe as etl
from etl import geo_pipe as geopipe
from cons.check_illegal_chars import IllegalCharacters
from cons.check_illegal_captials import IllegalCaptials
from cons.stop_with_multi_road_names import MultiRoadName
from cons.localities_with_identical_stops import LocalitiesIDStops
from cons.check_illegal_spaces import IllegalSpaces
from cons.stop_missing_bearing import BearingMissing
from cons.stop_name_contains_locality import NameContainsLocality
from cons.stop_name_length import CheckName
from cons.stop_name_with_high_risk_words import StopNameHighRisks
from cons.stop_in_different_named_admin_area import StopsDifferentNamedAdminArea
from cons.atcocode_check import AtcocodeCheck
from cons.check_datetime import CheckDateTime
from cons.naptan_data_structure import NaptanStructureChecks
from geos.stops_in_the_water import CoastlineStops
from visualise.visualiser import generate_base_map
import click
import timeit
from pathlib import Path
from datetime import datetime


timestr = datetime.now().strftime("%Y_%m_%d")
dl_home = Path(Path.home() / "Downloads")


@click.command()
@click.option(
    "--named_area",
    type=str,
    required=True,
    prompt="Enter an administrative area level name.",
    help="Provide the correct name from the administrative area list\
              .",
)
def main(named_area):
    """Downloads the naptan dataset and runs the basic internal
    consistency checks and geospatial checks"""
    # etl pipeline functions.
    etl.naptan_data_source("nptg", "csv")
    etl.naptan_data_source("naptan_nodes", "csv")
    nodes = Path(f"{dl_home}/{timestr}_naptan_nodes.zip")
    nptg = Path(f"{dl_home}/{timestr}_nptg.zip")
    etl.extract_naptan_files(nodes)
    etl.extract_naptan_files(nptg)
    # naptanfilenames = etl.file_verification('ext')

    # dataframe creation
    gdf = etl.read_naptan_file("Stops")
    gdf = etl.deactivated_nodes(gdf)
    # we join the gazette locality code and admin code data onto the nodes data
    # frame, this gives us accurate locality and admin area names.
    locality_codes = etl.naptan_gazette_localities()
    gdf = etl.map_gazette_to_nodes(gdf, locality_codes, "NptgLocalityCode")
    admin_codes = etl.naptan_gazette_admin_area_codes()
    gdf = etl.map_gazette_to_nodes(gdf, admin_codes, "AdminCode")
    # we merge on the stop area data and corresponding codes for stop area
    gdf = etl.merge_stop_areas(gdf)
    gdf = geopipe.calculate_naptan_geometry(gdf)
    # Check that the naptan data structure downloaded is within acceptable
    # tolerances
    NaptanStructureChecks.check_naptan_stop_number_limits(gdf)
    # cli to provide a named administrative area within the naptan dataset.
    naptan_area_level = "AreaName"
    named_area = named_area
    # TODO or locality.
    # TODO make the named area geojson polygon with feature data.
    gdf_sub = etl.create_naptan_subframe(gdf, naptan_area_level, named_area)

    # Data Cleansing functions
    # illegal captials
    IllegalCaptials.check_illegal_caps(gdf_sub, "StopPoint")
    #  illegal characters
    IllegalCharacters.check_illegal_characters(gdf_sub, "StopPoint")
    # check for illegal spaces in required string columns.
    IllegalSpaces.check_illegal_spaces(gdf_sub)
    # The internal data consistency checks
    LocalitiesIDStops.localities_with_identical_stops(gdf_sub)
    NameContainsLocality.stop_name_contains_locality_name(gdf_sub)
    BearingMissing.stop_with_bearing_missing(gdf_sub)
    StopNameHighRisks.stop_names_with_high_risk_words(gdf_sub)
    StopsDifferentNamedAdminArea.stops_in_different_admin_area(gdf_sub)
    # TODO new checks - add to release notes
    CheckDateTime.check_stop_dates_not_after_today(gdf_sub)
    CheckName.check_name_length(gdf_sub)
    MultiRoadName.stop_with_multiple_road_names(gdf_sub, "CommonName")
    AtcocodeCheck.check_atcocode_length(gdf_sub)
    print("All internal consistency checks have been completed.")

    # geospatial data checks
    CoastlineStops.naptan_coastal_nodes(gdf_sub)
    #  checks that should only be performed on locality level, get passed out to
    # this function collection for running through the size of each type.
    etl.locality_level_checks(gdf_sub)
    # area specific checks
    print("All geospatial functions have been completed.")
    # make the map and populate with node cluster.
    generate_base_map(gdf_sub)
    return gdf_sub


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    exe_time = stop - start
    print(f"Program Executed in {str(exe_time)}")

# %%
kent

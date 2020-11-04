# %%
import os
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from zipfile import ZipFile

# data wrangling
import geopandas as gpd
from numpy.lib.utils import deprecate
import pandas as pd
import json
import numpy as np
import requests
from urllib.error import HTTPError

from etl import geo_pipe as geo
import cons


# config options
timestr = datetime.now().strftime("%Y_%m_%d")
dl_home = Path(Path.home() / 'Downloads')
node_dir = Path(f'{dl_home}/Naptan_Data/{timestr}_naptan_nodes/')
nptg_dir = Path(f'{dl_home}/Naptan_Data/{timestr}_nptg/')
geojson_dir = Path(f"{dl_home}/Naptan_Geojson/{timestr}_geojson/")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 5)
# declare geo coordinates conversion type.
crs = "EPSG:4326"


# %%
def stop_area_atcocode_identification(gdf):
    """[summary] identifies if which naptan stops are part of a stop group and
    which ones are not part of a stop group. A transform

    Args:
        gdf ([geopandas]): [description]

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]
        e: [description]
        ve: [description]
        OSError: [description]
        file_missing: [description]
        NotImplementedError: [description]
        NotImplementedError: [description]
        ve: [description]

    Returns:
        [type]: [description]
    """
    #
    stop_groups = gdf['StopAreaCode'].str[3:4].str.contains("g|G")
    #
    gdf_subset = gdf[stop_groups]
    return gdf_subset


# %%
def define_stops_areas(gdf,
                       loc_codes,
                       admin_codes):
    """[summary] Given combining a commonname and indicator with stop area data
    , you should be able to define what a stop area is. By using the ngpt data
    you can cross reference that to a specific locality.

    Args:
        gdf ([geopandas dataframe]): [description]
        loc_codes ([locality codes]): [description]
        admin_codes ([admin codes]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [gdf]: [A geopandas dataframe with stop area definitions.]
    """
    # TODO - this needs finishing, need to add nptg stop area data linkaging
    # functionality.
    gdf['stop_Area'] = gdf['StopPoint'] + loc_codes[''] + admin_codes['']

    return gdf
    raise NotImplementedError


# %%
def intersect_list_to_masks(df, col_name, value_list):
    """[summary] This is a filter function, that performs an inner join when
    given a list object and returns a filtered dataframe of the values in the
    given list. You must pass a valid column name and a valid list of strings
    expected in that column, will filter out all values not in the list
    from the given column, returning a dataframe with only the found entries,
    that match the list given values in the given column.

    Arguments:
        colName {[str]} -- [the pandas column name, as a string]
        value_list {[list]} -- [the list of strings to filter the dataframe.]

    Returns:
        [gdf] -- [a filtered gdf, with only the found list values within. ]
    """
    # uses numpy 1d intersection to filter an entire list of strings
    mask = df[col_name].apply(lambda x: np.intersect1d(x,
                                                       value_list).size > 0)
    failed_nodes = df[mask]
    return failed_nodes


# %%
def file_checker(file_locale, file_names, file_ext):
    """[summary] Lists the Naptan files available at the specificed location.
    If some files are missing/ or can't be open this should flag a warning.
    Arguments:

    Args:
        file_locale ([type]): [description]
        file_names ([type]): [description]
        file_ext ([type]): [description]

    Returns:
        [type]: [description]
    """
    # we print out if all the expected files are found and if so in the system
    # where.
    # making sure we let the user know what files have been found and where
    # if anything is missing we let them know that too.
    try:
        for expected in file_locale.iterdir():
            f = Path(f'{expected}')
            # check we can open the file, if this doesn't work, we know the
            # files are missing.
            fg = open(f)
            fg.close()
            # we check the files exist and are valid files of the expected type
            if f.exists and f.is_file and 'nptg' in str(file_locale):
                print(f'NPTG {f.stem} a {f.suffix} has been found.')
            # check for the node files
            elif 'nodes' in str(file_locale) and f.exists and f.is_file:
                print(f'Naptan Node {f.stem} {f.suffix} has been located.')
            else:
                sys.exit(f'Naptan file {f.stem} is missing.')
    except IOError:
        sys.exit(f'{file_locale} is not accessible.')
    except OSError:
        sys.exit(f'Naptan files {file_names} is wrong.')
    except ValueError as ve:
        sys.exit(f'{ve}')


# %%
def file_verification(ext):
    """[summary] runs file verification checks on the naptan and nptg
    files.

    Arguments:
        ext {[str]} -- [description]

    Raises:
        file_missing: [description]
        NotImplementedError: [description]
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """

    nptg_file_names = ['AdjacentLocality',
                       'AdminAreas',
                       'Districts',
                       'Localities',
                       'LocalityAlternativeNames',
                       'LocalityHierarchy',
                       'PlusbusMapping',
                       'PlusbusZones',
                       'Regions']

    naptan_file_names = ['AirReferences',
                         'AlternativeDescriptors',
                         'AreaHierarchy',
                         'CoachReferences',
                         'FerryReferences',
                         'Flexible',
                         'HailRide',
                         'LocalityMainAccessPoints',
                         'MetroReferences',
                         'RailReferences',
                         'StopAreas',
                         'StopAvailability',
                         'StopLocalities',
                         'StopPlusbusZones',
                         'Stops',
                         'StopsInArea']

    return file_checker(node_dir,
                        naptan_file_names,
                        ext), file_checker(nptg_dir,
                                           nptg_file_names,
                                           ext)


# %%
def folder_creator(folder):
    """[summary] Makes a folder if one for the given paths doesn't already
    exists.

    Args:
        folder ([Path]): [description]

    Returns:
        [path]: [Created folder at the given path.]
    """
    try:
        if not folder.exists():
            Path(f'{folder}').mkdir(parents=True,
                                    exist_ok=True)
            print(f"{folder} folder has being created.")

    except OSError as ose:
        sys.exit(f'{ose}')

    except FileExistsError:
        print(f'The {folder} file has been created.')

    except Exception as e:
        raise e
        sys.exit(f'{e} Report creation failed')
    finally:
        return folder


# %%
def downloader(file, url):
    """[summary] It checks the given datasource is accessible and if so downloads
    the files to the users download folder.

    Args:
        file ([str]): [The file (usually zip) we are downloading.]
        url ([str]): [The location of the file.]

    Raises:
        NotImplementedError: [exception support]
        ve: [description]
    """

    try:
        # let's check if the file exists already on the local system.
        if not file.exists():
            print(f'Downloading the {timestr} {file} Dataset.')
        else:
            return(f'{file} data for {timestr} has been downloaded.')
    # then defensively resolve our errors,
    except ConnectionError as ce:
        sys.exit(f' {ce} No internet connection was found.')
    except ConnectionRefusedError as cre:
        sys.exit(f'{cre} This system is not allowed to access the Naptan Site.')
    except HTTPError as httperror:
        sys.exit(f'{httperror} the Naptan download server is unavailable.')
    except ValueError as ve:
        raise ve
        sys.exit('Site is not valid.')

    finally:
        # assumes success of the above.
        dir = Path(dl_home, "/Naptan_Data/")
        response = requests.get(url)
        # we overwrite to avoid appending the same data multiple times to the
        # same file
        with open(os.path.join(dir, file), 'wb') as f:
            f.write(response.content)
            response.close()


# %%
def naptan_data_source(naptan_data,
                       format='csv',
                       local_authority_codes='None'):
    """[summary] As the Naptan and nptg can refer to different formats and 
    naptan can either be the whole dataset or a specific subset relating to a
    given local area authority.
    Args:
        naptan_data (str): [description]. Defaults to [].
        format (str, optional): [description]. Defaults to 'csv'.
        local_authority_code ([type], optional): [description]. 
        Defaults to None.
    Raises:
        NotImplementedError: [XML download is not currently supported.]
    """
    # base naptan path for nptg and naptan node data.
    base = 'http://naptan.app.dft.gov.uk/'
    try:
        file = Path(f'{dl_home}/{timestr}_{naptan_data}.zip')
        # let's check the file exists and is readable.
        if Path.exists(file) and file.stat().st_size != 0:
            print(f'Naptan Data for {timestr} has already been downloaded.')
        elif naptan_data == 'naptan_nodes':
            # base for just node data.
            naptan_base = f'{base}DataRequest/Naptan.ashx'
            # the below filters url creation to create a locality list codes.
            if local_authority_codes.isdigit():
                url = (f'{naptan_base}{format}&LA={local_authority_codes}')
            elif format == 'xml':
                # will just be the base url.
                url = naptan_base
            else:
                url = (f'{naptan_base}?format={format}')
            print(f'Downloading all Naptan Node {format} data.')
            return downloader(file, url)

        elif naptan_data == 'nptg':
            # downloads the nptg data.
            print(f'Downloading the {naptan_data} data.')
            file = Path(f'{dl_home}/{timestr}_{naptan_data}.zip')
            url = f'{base}datarequest/nptg.ashx?format={format}'
            return downloader(file, url)
    except OSError:
        raise OSError


# %%
def extract_naptan_files(zip_file):
    """[summary] Extracts the downloaded zip file.

    Arguments:
        zip_file {[path]} -- [description]
    """
    dest = Path(f'{dl_home}/Naptan_Data/{zip_file.stem}/')
    try:
        # Check that the directory exists, that it is a directory and it's not
        # empty.
        if dest.exists() and dest.is_dir() and any(Path(dest).iterdir()):
            print(f'Already Extracted {timestr} Naptan Data to {dest}.')
            pass
        if zip_file.is_file() and zip_file.suffix == '.zip':
            print(f'Extracting all {zip_file} files in archive.')
    except FileNotFoundError:
        folder_creator(Path(f'{dest}'))
        print(f'{dest.stem} folder is being created.')
    except FileExistsError:
        sys.exit('File already exists')
    except Exception as e:
        sys.exit(e)
    finally:
        with ZipFile(zip_file, "r") as zipobj:
            # Extract all the contents of zip file in the working directory
            zipobj.extractall(dest)
            print(f'Extracted all files to {dest}')


# %%
def deactivated_nodes(df):
    """[summary] - Returns a dataframe of only active, pending, or new nodes
    or deleted stops from the last 3 years, for representative sampling.
    deleted nodes are removed for the sake of this test. This test is also not,
    concerned with reporting errors, as this is a data cleaning function

    Arguments:
        df {[geopanda dataframe]} -- [The Naptan master dataframe.]

    Returns:
        [type] -- [description]
    """
    # TODO filter this to stops with a modification date time within the last 3
    # years so that there is a represenative sample of deactived stops.
    try:
        exp_date = (datetime.now() - timedelta(days=365*3))
        # we filter all the missing deleted stops that are older than 3 yrs.
        mask = ~((df['Status'] == 'del') &
                 (df['ModificationDateTime'] <= exp_date))
        active_nodes = df[mask]
        # TODO needs to be integrated with reporting function.
        # inactive_nodes = df[~mask]
        # rep.report_failing_nodes('Inactive Nodes',
        #                            inactive_nodes)
        return active_nodes
    except FileNotFoundError as file_missing:
        raise file_missing
        sys.exit(f'{file_missing}')


# %%
def load_gazette_adjanct_localities():
    """[summary]

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]
        ve: [description]

    Returns:
        [type]: [description]
    """

    columns = ['NptgLocalityCode',
               'AdjacentNptgLocalityCode']
    adjacent_local = pd.read_csv(f"{nptg_dir}/AdjacentLocality.csv",
                                 sep=',',
                                 low_memory=False,
                                 encoding='iso-8859-1',
                                 usecols=columns)
    return adjacent_local


# %%
def load_gazette_localities_alternative_names():
    """[summary]

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]
        ve: [description]

    Returns:
        [type]: [description]
    """

    columns = ['NptgLocalityCode', 'OldNptgLocalityCode', 'LocalityName',
               'LocalityNameLang', 'ShortName', 'ShortNameLang',
               'QualifierName', 'QualifierNameLang', 'QualifierLocalityRef',
               'QualifierDistrictRef']
    alternate_locals = pd.read_csv(f"{nptg_dir}/LocalityAlternativeNames.csv",
                                   sep=',',
                                   low_memory=False,
                                   encoding='iso-8859-1',
                                   usecols=columns)
    return alternate_locals


# %%
def load_gazette_locality_hierarchy():
    """[summary]

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]
        ve: [description]

    Returns:
        [type]: [description]
    """

    columns = ['ParentNptgLocalityCode',
               'ChildNptgLocalityCode']
    locality_hierarchy = pd.read_csv(f"{nptg_dir}/LocalityHierarchy.csv",
                                     sep=',',
                                     low_memory=False,
                                     encoding='iso-8859-1',
                                     usecols=columns)
    return locality_hierarchy


# %%
def load_gazette_plusbus_mapping():
    """[summary]

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]
        ve: [description]
    Returns:
        [type]: [description]
    """
    cols = ['PlusbusZoneCode', 'Sequence', 'GridType', 'Easting', 'Northing']
    plus_bus_map = pd.read_csv(f"{nptg_dir}/PlusbusMapping.csv",
                               sep=',',
                               low_memory=False,
                               encoding='iso-8859-1',
                               usecols=cols)
    return plus_bus_map


# %%
def load_gazette_plusbus_zones():
    """[summary] loads the naptan plus bus zone data, note that this data is 
    largely deprecated.

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]
        ve: [description]
    Returns:
        [type]: [description]
    """
    cols = ['PlusbusZoneCode',
            'Name',
            'NameLang',
            'Country']
    plus_bus_zones = pd.read_csv(f"{nptg_dir}/PlusbusZones.csv",
                                 sep=',',
                                 low_memory=False,
                                 encoding='iso-8859-1',
                                 usecols=cols)
    return plus_bus_zones


# %%
def naptan_gazette_districts():
    """[summary] loads the districts codes from the gazette files.

    Returns:
        [type] -- [description]
    """
    cols = ['AdministrativeAreaCode',
            'DistrictCode',
            'DistrictName']
    districts = pd.read_csv(f'{nptg_dir}/Districts.csv',
                            encoding='iso-8859-1',
                            low_memory=False,
                            usecols=cols)
    districts = districts.rename(columns={'AdministrativeAreaCode':
                                          'AdminCode'})
    return districts


# %%
def naptan_gazette_region():
    """[summary] loads the Region area codes from the gazette files.

    Returns:
        [type] -- [description]
    """
    cols = ['RegionName', 'RegionCode']
    region_codes = pd.read_csv(f'{nptg_dir}/Regions.csv',
                               encoding='iso-8859-1',
                               low_memory=False,
                               usecols=cols)
    return region_codes


# %%
def naptan_gazette_admin_area_codes():
    """[summary] loads the admin area codes from the gazette files.
    Using nptgcsv files as the source for linking the admin area codes with
    the nodes data. 

    Returns:
        [dataframe] -- [Contains the]
    """
    cols = ['AdministrativeAreaCode',
            'AtcoAreaCode',
            'AreaName',
            'ShortName',
            'RegionCode']
    aac = pd.read_csv(f'{nptg_dir}/AdminAreas.csv',
                      encoding='iso-8859-1',
                      low_memory=False,
                      usecols=cols)
    aac = aac.rename(columns={'AdministrativeAreaCode':
                              'AdminCode'})
    # pass the codes as strings not ints.
    aac['AdminCode'] = aac['AdminCode'].astype(str)
    return aac


# %%
def naptan_gazette_localities():
    """[summary] returns the gazette locality data for use with the stops
    data.
    """
    # just the basics
    cols = ['NptgLocalityCode',
            'LocalityName',
            'AdministrativeAreaCode',
            'QualifierName',
            'NptgDistrictCode',
            'SourceLocalityType',
            'GridType',
            'Easting',
            'Northing']
    # read the file
    gaz_locs = pd.read_csv(f'{nptg_dir}/Localities.csv',
                           encoding='iso-8859-1',
                           low_memory=True,
                           usecols=cols)
    # TODO -
    gaz_locs = gaz_locs.rename(columns={'AdministrativeAreaCode':
                                        'AdminCode'})
    gaz_locs['AdminCode'] = gaz_locs['AdminCode'].astype(str)
    # convert lat long
    gaz_locs = geo.convert_to_lat_long(gaz_locs)
    # calculate geometry point for geodataframe.
    gaz_locs = geo.calculate_naptan_geometry(gaz_locs)
    # rename for later merger.
    gaz_locs.rename(columns={'NptgLocalityCode': 'NptgLocalityCode',
                             'LocalityName': 'LocalityName',
                             'QualifierName': 'QualifierName',
                             'NptgDistrictCode': 'NptgDistrictCode',
                             'SourceLocalityType': 'SourceLocalityType',
                             'GridType': 'NptgGridType',
                             'Longitude': 'Gazette_Longitude',
                             'Latitude': 'Gazette_Latitude',
                             'geometry': 'Gazette_geometry'}, inplace=True)
    # TODO new column merge Locality and qualifier name, check if duplicate.
    gaz_locs['Qualified_Locality'] = gaz_locs['LocalityName'] + ', ' +\
        gaz_locs['QualifierName']
    return gaz_locs


# %%
def map_gazette_to_nodes(df, gazette_data, gazette_column):
    """[summary]maps the given gazette reference data and column to the naptan
     nodes data.

    Arguments:
        df {[geodataframe]} -- [the naptan dataframe]
        gazette_data {[gazette reference data]} -- []
        gazette_column {[pandas series column]} -- [the column we are joining 
        on.]

    Raises:
        NotImplemented: [description]

    Returns:
        [type] -- [description]
    """
    # capture the reference types we know are supporte
    if gazette_column == 'NptgLocalityCode':
        abr = 'Locality'
    else:  # gazette_column == 'AdminCode':
        abr = 'AAC'
    """
    else:
        raise NotImplementedError
        print('Gazette reference type not supported.')
    """

    mapped_df = pd.merge(df,
                         gazette_data,
                         how='left',
                         suffixes=('_df', f'_{abr}'),
                         on=[f'{gazette_column}'])
    # we drop them here, so that order is irrelevant for node mapping.
    dropcols = ['Easting', 'Northing', 'MaximumLengthForShortNames ',
                'LocalityName_df', 'Gazette_Longitude', 'Gazette_Latitude',
                'National', 'ContactEmail', 'ContactTelephone', 'AreaNameLang',
                'ShortName', 'ShortNameLang', 'Notes', 'NotesLang',
                'Gazette_geometry', 'geometry_Locality', 'AdminCode_Locality']
    # remove the duplicated columns.
    mapped_df = mapped_df.drop(dropcols,
                               axis=1,
                               errors='ignore')
    # fixes singular locality name column
    mapped_df = mapped_df.rename({'LocalityName_Locality': 'LocalityName',
                                  'geometry_df': 'geometry',
                                  'AdminCode_df': 'AdminCode'},
                                 axis=1)
    return mapped_df


# %%
def read_naptan_file(file_name):
    """Description: Reads the presented dataset using Panda, manages the memory
     issue if the stop file is being ingested. No NaPTAN other files require 
     memory management.

        Args:
            file_name: the csv file containing naptan data. 

        Returns:
            returns a pandas dataframe containing geo naptan data.
    """

    file_path = Path((f"{node_dir}/{file_name}.csv")).resolve()
    # Enforces Dtype of datetime objects on required columns"""
    parse_dates = ["CreationDateTime", "ModificationDateTime"]
    # set missing values for ingestion fields
    # missing_values = ["n/a", "na", "--", "NaN"]
    # elegantly grabs file name for outfile use.
    fields = ['ATCOCode', 'NaptanCode', 'PlateCode', 'CleardownCode',
              'CommonName', 'CommonNameLang', 'ShortCommonName',
              'ShortCommonNameLang', 'Landmark', 'LandmarkLang', 'Street',
              'StreetLang', 'Crossing', 'CrossingLang', 'Indicator',
              'IndicatorLang', 'Bearing', 'NptgLocalityCode', 'LocalityName',
              'ParentLocalityName', 'GrandParentLocalityName', 'Town',
              'TownLang', 'Suburb', 'SuburbLang', 'LocalityCentre', 'GridType',
              'Longitude', 'Latitude', 'StopType',
              'BusStopType', 'TimingStatus', 'DefaultWaitTime', 'Notes',
              'NotesLang', 'AdministrativeAreaCode', 'CreationDateTime',
              'ModificationDateTime', 'RevisionNumber', 'Modification',
              'Status']

    if file_name.lower() == ('stopareas'):
        print(f'Currently loading the {file_path.stem} file.')
        cols = ['StopAreaCode', 'Name', 'NameLang', 'CreationDateTime',
                'AdministrativeAreaCode', 'StopAreaType', 'GridType',
                'Easting', 'Northing', 'ModificationDateTime', 'Status']
        gdf = pd.read_csv(file_path, sep=',', encoding='ISO-8859-1',
                          verbose=False, na_filter=False,
                          infer_datetime_format=True, usecols=cols,
                          parse_dates=parse_dates,
                          engine='c')
        # lat long coordinates after reading.
        gdf = geo.convert_to_lat_long(gdf)

    elif file_name.lower() == ('stopsinarea'):
        print(f'Currently loading the {file_path.stem} file.')
        cols = ['StopAreaCode', 'AtcoCode', 'ModificationDateTime',
                'CreationDateTime']
        gdf = pd.read_csv(file_path, sep=',', encoding='ISO-8859-1',
                          verbose=False, na_filter=False,
                          infer_datetime_format=True, usecols=cols,
                          parse_dates=parse_dates,
                          engine='c')
        # so are stop areas will merge with nodes.
        gdf = gdf.rename(columns={'AtcoCode': 'ATCOCode'})

    elif file_name.lower() == ('stops'):
        print('Currently loading the stops file this may take some time.')
        gdf = pd.read_csv(file_path, sep=',', low_memory=False,
                          encoding='ISO-8859-1', verbose=False,
                          infer_datetime_format=True,
                          na_filter=False, usecols=fields,
                          parse_dates=parse_dates,
                          engine='c')
        # we need the stoppoint name for stop area calculations.
        gdf['StopPoint'] = gdf['CommonName'] + ' ' + gdf['Indicator']
        # we rename and cast the admin area code column to a str
        gdf = gdf.rename(columns={'AdministrativeAreaCode': 'AdminCode'})
        gdf['AdminCode'] = gdf['AdminCode'].astype(str)
        # we probably don't want to calculate geometry here, as it will never
        #  be used on the whole uk landmass.

    else:
        print(f'Currently loading the {file_path.stem} file.')
        gdf = pd.read_csv(file_path, sep=',', encoding='ISO-8859-1',
                          header='infer', verbose=False, na_filter=False,
                          infer_datetime_format=True,
                          parse_dates=parse_dates,
                          engine='c')
    return gdf


# %%
def merge_stop_areas(gdf):
    """[summary] to determine the stop areas that apply to nodes within the 
    the stop area, we need to merge the stops file with stops area, and stops 
    in areas. This is done below.

    Args:
        gdf ([type]): [description]
        stops_areas ([type]): [description]
        stops_in_area ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """

    # merge together the stop in areas and stoparea dataframes.
    stopinarea = read_naptan_file('StopsInArea')
    stopareas = read_naptan_file('StopAreas')
    stop_areas_nodes = pd.merge(stopinarea,
                                stopareas,
                                how='left',
                                on='StopAreaCode')
    # this is clearing from the merge.
    stop_areas_nodes = stop_areas_nodes.drop(columns=['CreationDateTime_y',
                                                      'ModificationDateTime_y',
                                                      'CreationDateTime_x',
                                                      'ModificationDateTime_x',
                                                      'AdministrativeAreaCode',
                                                      'NameLang'],
                                             axis=1)
    # should be false
    stop_areas_nodes.ATCOCode.duplicated().any()
    # should be true
    stop_areas_nodes.StopAreaCode.duplicated().any()
    # now we merge on to the stops node frame so we have a complete list of all
    # stop areas.
    gdf = pd.merge(gdf,
                   stop_areas_nodes,
                   indicator=True,
                   how='left',
                   on='ATCOCode',
                   suffixes=('', '_area'))
    gdf = gdf.rename(columns={'Name': 'StopAreaName'})

    return gdf


# %%
def non_standard_stop_area_generation(df):
    """[summary] use the stop point type data to match nodes to the relevant,
    stop area, using the primary stop area matching table on pg 53 of the 
    below,
    http://naptan.dft.gov.uk/naptan/schema/2.5/doc/NaPTANSchemaGuide-2.5-v0.67.pdf

    Arguments:
        df_subframe {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    # TODO this is really ugly code, do a vectorisation or something.
    Ferries = df[df['StopType'].str.contains('FTD|FER|FBT')]
    # TODO -> filter down into dataframes containing
    # df['StopAreaType'] = df.loc[df['StopType'] ]
    Airports = df[df['StopType'].str.contains('AIR|GAT')]
    Railstation = df[df['StopType'].str.contains('RSE|RLY|RPL')]
    MetroTram = df[df['StopType'].str.contains('TMU|MET|PLT')]
    BusesStation = df[df['StopType'].str.contains('BCE|BST|BCQ|BCS|MKD')]
    BusStreet = df[df['StopType'].str.contains('BCT|MKD|CUS|HAR|FLX')]
    Taxis = df[df['StopType'].str.contains('TXR')]
    Telcabinet = df[df['StopType'].str.contains('LSE|LCB|LPL')]
    CarPickup = df[df['StopType'].str.contains('SDA')]
    return Ferries, Airports, Railstation, MetroTram, BusesStation, BusStreet,
    Taxis, Telcabinet, CarPickup


# %%
def get_naptan_columns(filename):
    """Description:
        We need to pass the query reader some naptan column index data so that
        we can avoid some nasty sql injections.
        Args:
            [type] -- [filename]

        Returns:
            naptanCols:
    """
    file_path = Path((f"{node_dir}{filename}.csv")).resolve()
    dfcsv = pd.read_csv(file_path,
                        encoding='iso-8859-1')
    naptan_cols = dfcsv.columns
    return naptan_cols


# %%
# source url 'http://naptan.app.dft.gov.uk/Reports/frmStopsSummaryReport'
def get_atcocode_table(url):
    """Description: download atcocode table codes
        Args: 'http://naptan.app.dft.gov.uk/Reports/frmStopsSummaryReport'
        Returns:
    """
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    atco_File = df.to_csv('./atco_code_lookup.csv',
                          encoding='utf-8',
                          sep=',')
    return atco_File


# %%
def clean_atcocode_table(atco_File):
    """[summary]:- Cleans up the atcocode table data.
    """
    atcocode_cols = ['Region',
                     'Area_Name',
                     'Atco_Prefix',
                     'Active_Stops',
                     'Active_StopAreas']
    df = pd.read_csv(atco_File,
                     sep='\t',
                     encoding='utf-8',
                     usecols=atcocode_cols,
                     names=atcocode_cols)
    # We just want to clean up the messy import of the column names and types.
    df = df[~df['Region'].str.contains('Region', na=False)]
    df['Atco_Prefix'] = df['Atco_Prefix'].astype(int)
    df.reset_index(drop=True, inplace=True)
    cleaned_atco_file = df.to_csv('./cleaned_atco_code_lookup.csv',
                                  encoding='utf-8',
                                  usecols=atcocode_cols,
                                  sep=',')
    return cleaned_atco_file


# %%
def read_atcocode_table(atco_file):
    """[summary] reads a cleaned version of the atcocode file.

    Arguments:
        atco_File {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    atcocode_cols = ['Region',
                     'Area_Name',
                     'Atco_Prefix',
                     'Active_Stops',
                     'Active_StopAreas']
    atcocodes = pd.read_csv(atco_file, sep='\t',
                            encoding='utf-8', usecols=atcocode_cols,
                            names=atcocode_cols)
    atcocodes = atcocodes[~atcocodes['Region'].str.contains(
        'Region', na=False)]
    atcocodes['Atco_Prefix'] = atcocodes['Atco_Prefix'].astype(int)
    return atcocodes


# %%
def wrangle_stop_area_matrix(stop_area_matrix):
    """[returns a stop area matrix and cleanse the table.]

    Returns:
        [a filepath object] -- [the filename of the Stop Area Matrix.]
    """
    stop_area_matrix_file = Path(dl_home,
                                 (f"{stop_area_matrix}.csv")).resolve()
    df = pd.read_csv(stop_area_matrix_file,
                     encoding='utf-8',
                     sep=',',
                     names=['Group', 'Mode', 'Description', 'Entrance',
                            'Access Area', 'Bay / Pole', 'Sub Type',
                            'Primary Area'])
    return df


# %%
def create_naptan_subframe(gdf, naptan_area_level, col_value):
    """[summary] creates a naptan sub frame based on a given column name,
     by the value that is presented must be in that column.

    Arguments:
        gdf {[geopandas dataframe]} -- [the naptan dataframe]
        naptan_area_level {[str]} -- [the name of the column which will split
        the dataframe on]
        colvalue {[str]} -- [the value in the column to query.]

    Returns:
        [geodataframe] -- [The naptan subframe]
    """

    # convert the colvalue string into a lower case.
    try:
        if isinstance(col_value, str):
            pass
    except isinstance(col_value, int):
        col_value = f'{col_value}'
    finally:
        col_value = col_value.lower()

    lower_case = gdf[naptan_area_level].str.lower()
    new_df = pd.DataFrame(lower_case)
    gdf.update(new_df)
    # we put this here so we can filter out all areas that are managed by
    # dft centrally
    dft_authorities = ['National - National Rail',
                       'National - National Air',
                       'National - National Ferry',
                       'National - National Tram']
    # for grouping we need to pass in wildcard values, ideally string
    #  contains but the stop area code will always start with the atcocode for
    # the area or mode.
    if naptan_area_level == 'AreaName':
        # check if an invalid area has been passed.
        try:
            if col_value in dft_authorities:
                # if the user passes in a DfT managed area, we exit out
                sys.exit(f'{col_value} is a DfT central authority.')

        except KeyError:
            # catch the value if isn't found.
            sys.exit(f"{col_value} was not found in the given dataframe.")

        finally:
            # We get the nptg locality codes within the given admin area, as
            # this will include all forms of transport for the area and not
            # just bus transport infrastructure.
            gdf_sub = gdf[gdf[f'{naptan_area_level}'] == col_value]
            gdf_subframe = geo.calculate_naptan_geometry(gdf_sub)
            return gdf_subframe

    elif naptan_area_level == 'StopType':
        try:
            gdf1 = gdf[gdf['StopType'].str.match(col_value)]
            gdf_subframe = geo.calculate_naptan_geometry(gdf1)
            return gdf_subframe
        except KeyError:
            # catch of the value just isn't found.
            sys.exit(f"{col_value} is not known stoptype.")

    elif naptan_area_level == 'StopAreaCode':
        mask = gdf[f'{naptan_area_level}'].str.startswith(f'{col_value}')
        gdf_subframe = gdf[mask]
        gdf_sub = geo.calculate_naptan_geometry(gdf_subframe)
        return gdf_sub

    # expects the full string of the npgt or admin code to work.
    elif naptan_area_level == 'NptgLocalityCode' or 'LocalityName':
        # print('This is a locality area.')
        columngroup = gdf.groupby(naptan_area_level)
        gdf_subframe = columngroup.get_group(col_value)
        gdf_subframe.reset_index(drop=True,
                                 inplace=True)
        gdf_sub = geo.calculate_naptan_geometry(gdf_subframe)
        return gdf_sub
    else:
        sys.exit('Column type is not supported.')


# %%
def create_subframe_for_stopareacode(df, colvalue):
    """[summary] The Stop Area Code is important for working out stop areas,
    Creating a subframe for it, requires some careful thinking,
    this function; 
    1) take in the stop area code dataframe, and other related frames,
    if necessary, 
    2) based on the colvalue, filter search the last part of the stop area code
    column for the associate values.
    3) creates a naptan sub frame based on a column name, by a given
    value that must be in that column.

    Arguments:
        df {[type]} -- [the naptan dataframe]
        colvalue {[type]} -- [the value in the column to split on.]

    Returns:
        [type] -- [description]
    """

    # for grouping we need to pass in wildcard values, prefer strings
    # contains but the stop area code will always start with the atcocode for
    # the area or mode.
    df['EventCnt'] = df['StopAreaCode'].apply(len)
    highest = df['EventCnt'].max()
    lowest = df['EventCnt'].max() - df['EventCnt'].min()
    df['StopAreaCodes_id'] = df['StopAreaCode'].str[3:]
    mask = df['StopAreaCode'].str.startswith(f'{colvalue}')
    df_subframe = df[mask]
    return df_subframe
    raise NotImplementedError


# %%
def group_naptan_datatypes(gdf, naptan_column='LocalityName'):
    """[summary] groups together naptan datasets into subsets that are grouped
    by the given naptan column.

    Args:
        gdf ([type]): [description]
        naptan_column (str, optional): [description]. Defaults to 'LocalityName'.

    Returns:
        [type]: [description]
    """
    # collapse dataset to minimum, keeping possibly useable datasets
    gdf2 = gdf[['LocalityName',
                'NptgLocalityCode',
                'AreaName',
                'StopAreaCode',
                'Latitude',
                'Longitude']]
    # calculates the centroid of each given naptan segment.
    gdf3 = gdf2.groupby([naptan_column], as_index=False)[
        ['Latitude', 'Longitude']].apply(lambda x: np.mean(x, axis=0))
    # convert the lat lon into centroid geometry points.
    gdf4 = geo.calculate_naptan_geometry(gdf3)
    # save output to csv.
    gdf4.to_csv(f'{naptan_column}.csv',
                encoding='utf-8',
                sep=',')
    return gdf4


# %%
def locality_level_checks(gdf):
    """[summary] to be used for when geodata is provided for a given area, 
    admin area, locality, or stop area or smaller. the below checks should be 
    performed on subsets of naptan, not the entire dataset.

    Args:
        gdf ([geopandas]): []
    """
    try:
        # we get the size here for later checking.
        naptan_size = gdf.shape
        # The below functions should only be run on an admin area level or
        # lower
        if naptan_size[0] >= 1000:
            print('This is an admin area.')
            print('Not all Geospatial checks can be run against an area of this size.')
        # the below functions should only be run on a locality level or lower
        elif naptan_size[0] <= 300:
            print('Checking locality currently')
            # checking the localites
            cons.Localities_with_Identical_Stops(gdf)
            # check if
            print(
                f"Not all road names match coordinates for {gdf.AreaName.unique}")
            geo.road_name_matches_coordinates(gdf)

        # the below functions should only be run on a stop area level or lower
        elif naptan_size[0] <= 30:
            print('This is a stop area or a stop.')
            #
            geo.get_nearest_road_name(gdf)
        else:
            print('Naptan Geodata shape is irregular.')
    except Exception as e:
        sys.exit('Given naptan file is too large to process.')
        print(e)

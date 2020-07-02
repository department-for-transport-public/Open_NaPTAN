# %%
import os
import sys
from collections import Counter
from datetime import datetime, timedelta
from glob import glob
from pathlib import Path
from zipfile import ZipFile

# data wrangling
import geopandas as gpd
import pandas as pd
import numpy as np
import requests
from urllib.error import HTTPError
# data maniuplation
from convertbng.util import convert_lonlat
# logging
from shapely.geometry import Point

import con_checks as con
import geo_checks as geo


# %%
timestr = datetime.now().strftime("%Y_%m_%d")

src_home = Path('./OpenNaPTAN/src/')
data_home = Path('./OpenNaPTAN/data/')
base_path = (f'{os.getcwd()}')
download_home = str(os.path.join(Path.home(), "Downloads"))
naptan_csv_url = 'http://naptan.app.dft.gov.uk/DataRequest/Naptan.ashx?format=csv'
naptan_xml_url = 'http://naptan.app.dft.gov.uk/Datarequest/naptan.ashx'

# config options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 5)


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
    mask = df[col_name].apply(lambda x: np.intersect1d(x, value_list).size > 0)
    failed_nodes = df[mask]
    return failed_nodes


# %%
def downloads_naptan_data(format='csv', local_authority_code=''):
    """[summary]  Downloads naptan csv files from the app.dft.gov.uk site. 
    Assumes no longer is required for accessing the data this route.

    Args:
        format (str, optional): [description]. Defaults to 'csv'.
        local_authority_code (str, optional): [description]. Defaults to ''.

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]
        ve: [description]
    """

    dir = str(os.path.join(Path.home(), "Downloads"))
    file = Path(f'{download_home}/{timestr}_Naptan_Data.zip')

    try:
        # let's check if the naptan zip file exists.
        if not file.exists():
            print('Downloading the entire Naptan Dataset.')
            url = 'http://naptan.app.dft.gov.uk/DataRequest/Naptan.ashx?format=csv'
            response = requests.get(url)
            with open(os.path.join(dir, file), 'wb') as f:
                f.write(response.content)
                response.close()

        # the below isn't supported yet.
        elif local_authority_code.isdigit():
            url = (f'http://naptan.app.dft.gov.uk/DataRequest/Naptan.ashx?format={format}&LA={local_authority_code}')
            raise NotImplementedError
        # the below isn't support yet.
        elif format == 'xml':
            url = (f'http://naptan.app.dft.gov.uk/DataRequest/Naptan.ashx?format={format}&LA={local_authority_code}')
            raise NotImplementedError
        else:
            return(f'Naptan Data has been for {timestr} has been downloaded.')

    except ConnectionError as ce:
        sys.exit(f' {ce} No internet connection was found.')
    except ConnectionRefusedError as cre:
        sys.exit(f'{cre} This system is not allowed to access the Naptan Site.')
    except HTTPError as httperror:
        sys.exit(f'{httperror} the Naptan download server is unavailable.')
    except ValueError as ve:
        raise ve
        sys.exit('Site is not valid.')


# %%
def extract_naptan_files():
    """[summary] Extracts the downloaded naptan zip file.

    Arguments:
        naptanzipfile {[type]} -- [description]
        dest_dir {[type]} -- [description]
    """

    zip_file = Path(f'{download_home}/{timestr}_Naptan_Data.zip')
    destination = Path(f'{os.getcwd()}/data/{timestr}_Naptan_Data')
    try:
        if zip_file.is_file() and zip_file.suffix == '.zip':
            with ZipFile(zip_file, "r") as zipobj:
                # Extract all the contents of zip file in the working directory
                zipobj.extractall(destination)
                print(f'Extracting all {destination} files in archive.')
    except FileNotFoundError:
        sys.exit('Naptan archive file not found.')
    except FileExistsError:
        sys.exit('File already exists')
    except Exception as e:
        sys.exit(e)


# %%
def check_naptan_files():
    """[summary] Lists the Naptan files available at the specificed location.
    If some files are missing/ or can't be open this should flag a warning.
    Arguments:
        file_list_location {[Path]} -- [description]
        file_ext {[file extension]} -- [description]

    Returns:
        [type] -- [description]
    """
    # TODO check if files are readable
    file_list_location = (f'{os.getcwd()}/data/{timestr}_Naptan_Data/')
    file_ext = 'csv'
    expected_file_names = ['AirReferences',
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

    naptan_file_names = []
    # we print out if all the expected files are found and if so in the 
    # system where.
    for expected in expected_file_names:
        npfile = Path(f'{file_list_location}{expected}.{file_ext}')
        if npfile.is_file() and npfile.exists():
            naptan_file_names.append(npfile.stem)
            print(f'{npfile.name} as a {file_ext} has been found.')
        else:
            print(f'The {npfile} is missing or the file extension is wrong.')


# %%
def convert_xml_to_df(xml_doc):
    # TODO -- convert xml into a pandas dataframe for easier verification.
    """ Description: We can take in the naptan data as a 
        Args: xml_doc
        Returns: returns a panda dataframe of the xml document.
    """
    attr = xml_doc.attrib
    doc_dict = pd.DataFrame
    for xml in xml_doc.iter('document'):
        doc_dir = attr.copy()
        doc_dir.update(xml.attrib)
        doc_dict['data'] = xml.text
    return doc_dict


# %%
def file_pep8_cleaning(home, ext):
    """Description: takes a directory and file extension and then renames them
                 according to 

        Args:
            home: the target directory, only one at once
            ext: a file type extension, only one at once
        Returns:

    """
    home = Path(home)
    os.chdir(home)
    flist = []
    for p in Path().iterdir():
        if (p.is_file() and p.suffix == ext):
            g = Path(p).stem
            flist.append(g)
            h = string.capwords(g)
            i = h.title()
            j = '_'.join([s[0].upper() + s[1:] for s in i.split(' ')])
            to_file = Path(home, j)
            flist.append(to_file)
            p.rename(to_file)
    with open((home, 'update_list.txt'), 'w+') as file:
        file.write(flist)


# %%
def convert_to_lat_long(df):
    """Descriptions: Converts 100,000+ coordinates in a dataframe
     into accurate longitude and latitude adding the columns where they are
     missing from a dataframe.

    Arguments:
        df {[type]} -- [description]
        file_name {[type]} -- [description]
    """
    easting_np = np.array(df.Easting)
    northing_np = np.array(df.Northing)
    res_list_np = convert_lonlat(easting_np, northing_np)
    df['Longitude'], df['Latitude'] = res_list_np[0], res_list_np[1]
    # drop the easting and northing columns, now we are done with them.
    df = df.drop(columns=['Easting', 'Northing'], axis=1)
    return df


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
        # report.nodes_error_reporting('Inactive Nodes',
        #                            inactive_nodes)
        return active_nodes
    except FileNotFoundError as file_missing:
        raise file_missing
        sys.exit(f'{file_missing}')


# %%
def calculate_naptan_geometry(df):
    """[summary] Takes in a dataframe and returns a dataframe
    with a geometry column calculate from using lat and lon CRS.
    """
    try:
        geom_list = [Point(lon, lat) for lon, lat in zip(df["Longitude"],
                                                         df["Latitude"])]
        gdf = gpd.GeoDataFrame(df,
                               geometry=geom_list,
                               crs={"init": "EPSG:4326"})
        return gdf

    except ValueError:
        print('Value Error could not be converted.')
        pass
    else:
        print('Naptan Geometry conversion failed.')


# %%
def get_centroid_naptan_area(df):
    """[summary] to determine where the folium map should be centred, when
    generating an ipython view.

    Arguments:
        df_subframe {[type]} -- [description]

    Returns:
        [rep_centroid] -- [a fix within geometry point, representative of
        all the points in the area.]
    """
    length = df['Geometry'].shape[0]
    sum_x = np.sum(df['Latitude'])
    sum_y = np.sum(df['Longitude'])
    cen_x, cen_y = sum_x/length, sum_y/length
    return cen_x, cen_y


# %%
def naptan_gazette_districts():
    """[summary] loads the districts codes from the gazette files.

    Returns:
        [type] -- [description]
    """
    cols = ['AdminAreaCode', 'DistrictCode', 'DistrictName']
    District_Codes = pd.read_csv(f'{os.getcwd()}/nptgcsv/Districts.csv',
                                 encoding='iso-8859-1',
                                 usecols=cols)
    return District_Codes


# %%
def naptan_gazette_region():
    """[summary] loads the Region area codes from the gazette files.

    Returns:
        [type] -- [description]
    """
    cols = ['RegionName', 'RegionCode']
    region_codes = pd.read_csv(f'{os.getcwd()}/nptgcsv/Regions.csv',
                               encoding='iso-8859-1',
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
    cols = ['AdministrativeAreaCode', 'AtcoAreaCode',
            'AreaName', 'ShortName', 'RegionCode']
    aac = pd.read_csv(f'{os.getcwd()}/nptgcsv/AdminAreas.csv',
                      encoding='iso-8859-1',
                      usecols=cols)
    aac = aac.rename(columns={'AdministrativeAreaCode': 'AdminAreaCode'})
    aac['AdminAreaCode'] = aac['AdminAreaCode'].astype(str)

    return aac


# %%
def naptan_gazette_localities():
    """[summary] returns the gazette locality data for use with the stops
    data. 
    """
    cols = ['NptgLocalityCode', 'LocalityName', 'AdministrativeAreaCode',
            'QualifierName', 'NptgDistrictCode', 'SourceLocalityType',
            'GridType', 'Easting', 'Northing']
    gaz_locs = pd.read_csv(f'{os.getcwd()}/nptgcsv/Localities.csv',
                           encoding='iso-8859-1',
                           usecols=cols)
    gaz_locs = gaz_locs.rename(columns={'AdministrativeAreaCode': 'AdminAreaCode'})
    gaz_locs['AdminAreaCode'] = gaz_locs['AdminAreaCode'].astype(str)
    gaz_locs = convert_to_lat_long(gaz_locs)
    gaz_locs = calculate_naptan_geometry(gaz_locs)
    gaz_locs.rename(columns={'NptgLocalityCode': 'NptgLocalityCode',
                                'LocalityName': 'LocalityName',
                                'AdminAreaCode': 'AdminCode',
                                'QualifierName': 'QualifierName',
                                'NptgDistrictCode': 'NptgDistrictCode',
                                'SourceLocalityType': 'SourceLocalityType',
                                'GridType': 'NptgGridType',
                                'Longitude': 'Gazette_Longitude',
                                'Latitude': 'Gazette_Latitude',
                                'Geometry': 'Gazette_geometry',
                                }, inplace=True)
    return gaz_locs


# %%
def map_gazette_data_to_nodes(df, gazette_data, gazette_column):
    """[summary]maps the given gazette reference data and column to the naptan
     nodes data.

    Arguments:
        df {[type]} -- [the naptan dataframe]
        gazette_data {[gazette reference data]} -- []
        gazette_column {[pandas series column]} -- [description]

    Raises:
        NotImplemented: [description]

    Returns:
        [type] -- [description]
    """
    # capture the reference types we know are supporte
    if gazette_column == 'NptgLocalityCode':
        abr = 'Locality'
    elif gazette_column == 'AdminAreaCode':
        abr = 'AAC'
    else:
        raise NotImplementedError
        print('Gazette reference type not supported.')

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
                'Gazette_geometry', 'geometry_Locality']
    # remove the duplicated columns.
    mapped_df = mapped_df.drop(dropcols,
                               axis=1,
                               errors='ignore')
    # fixes singular locality name column
    mapped_df = mapped_df.rename({'LocalityName_Locality': 'LocalityName',
                                  'geometry_df': 'Geometry'},
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
    base_path = (f'data/{timestr}_Naptan_Data')
    file_path = Path(base_path, (f"{file_name}.csv")).resolve()
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
        gdf = convert_to_lat_long(gdf)

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
        gdf = gdf.rename(columns={'AdministrativeAreaCode': 'AdminAreaCode'})
        gdf['AdminAreaCode'] = gdf['AdminAreaCode'].astype(str)
        gdf = calculate_naptan_geometry(gdf)

    else:
        print(f'Currently loading the {file_path.stem} file.')
        gdf = pd.read_csv(file_path, sep=',', encoding='ISO-8859-1',
                          header='infer', verbose=False, na_filter=False,
                          infer_datetime_format=True,
                          parse_dates=parse_dates,
                          engine='c')
    return gdf


# %%
def create_stop_areas(gdf):
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
    gdf = gdf.rename(columns={'Name': 'Stop_Area_Name'})

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
    base_path = (f'{os.getcwd()}/Naptan_Data_{timestr}/')
    file_path = Path(base_path, (f"{filename}.csv")).resolve()
    dfcsv = pd.read_csv(file_path, encoding='iso-8859-1')
    naptanCols = dfcsv.columns
    return naptanCols


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
    atco_File = df.to_csv('./atco_code_lookup.csv', encoding='utf-8', sep=',')
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
    df = pd.read_csv(atco_File, sep='\t', encoding='utf-8',
                     usecols=atcocode_cols, names=atcocode_cols)
    # We just want to clean up the messy import of the column names and types.
    df = df[~df['Region'].str.contains('Region', na=False)]
    df['Atco_Prefix'] = df['Atco_Prefix'].astype(int)
    df.reset_index(drop=True, inplace=True)
    cleaned_atco_File = df.to_csv('./cleaned_atco_code_lookup.csv',
                                  encoding='utf-8',
                                  usecols=atcocode_cols,
                                  sep=',')
    return cleaned_atco_File


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
    atcocodes = atcocodes[~atcocodes['Region'].str.contains('Region', na=False)]
    atcocodes['Atco_Prefix'] = atcocodes['Atco_Prefix'].astype(int)
    return atcocodes


# %%
def wrangle_stop_area_matrix(stop_area_matrix):
    """[returns a stop area matrix and cleanse the table.]

    Returns:
        [a filepath object] -- [the filename of the Stop Area Matrix.]
    """
    base_path = f"{os.getcwd()}tables/"
    stop_area_matrix_file = Path(base_path,
                                 (f"{stop_area_matrix}.csv")).resolve()
    df = pd.read_csv(stop_area_matrix_file,
                     encoding='utf-8',
                     sep=',',
                     names=['Group', 'Mode', 'Description', 'Entrance',
                            'Access Area', 'Bay / Pole', 'Sub Type',
                            'Primary Area'])
    return df


# %%
def create_naptan_subframe(gdf, naptan_area_level, colvalue):
    """[summary] creates a naptan sub frame based on a given column name,
     by the value that is presented must be in that column.

    Arguments:
        gdf {[geopandas dataframe]} -- [the naptan dataframe]
        naptan_area_level {[str]} -- [the name of the column which will split
        the dataframe on]
        colvalue {[str]} -- [the value in the column to split on.]

    Returns:
        [geodataframe] -- [The naptan subframe]
    """

    # convert the colvalue string into a lower case.
    colvalue = colvalue.lower()
    lower_case = gdf[naptan_area_level].str.lower()
    new_df = pd.DataFrame(lower_case)
    gdf.update(new_df)
    # we put this here so we can filter out all.
    dft_authorities = ['National - National Rail',
                       'National - National Air',
                       'National - National Ferry',
                       'National - National Tram']
    # for grouping we need to pass in wildcard values, ideally string
    #  contains but the stop area code will always start with the atcocode for
    # the area or mode.
    if naptan_area_level == 'AreaName':  # or 'AdminAreaCode' 
        # check if an invalid area has been passed.
        try:
            dft_authorities = ['National - National Rail',
                               'National - National Air',
                               'National - National Ferry',
                               'National - National Tram']
            if colvalue in dft_authorities:
                # if the user passes in a DfT managed area, we exit out
                sys.exit(f'{colvalue} is a DfT central authority.')

        except KeyError:
            # catch the value if isn't found.
            sys.exit(f"{colvalue} was not found in the given dataframe.")

        finally:
            # We get the nptg locality codes within the given admin area, as
            # this will include all forms of transport for the area and not
            # just bus transport infrastructure.
            gdf_subframe = gdf[gdf[f'{naptan_area_level}'] == colvalue]
            return gdf_subframe

    elif naptan_area_level == 'StopType':
        try:
            gdf1 = gdf[gdf['StopType'].str.match(colvalue)]
            return gdf1
        except KeyError:
            # catch of the value just isn't found.
            sys.exit(f"{colvalue} is not known stoptype.")

    elif naptan_area_level == 'StopAreaCode':
        mask = gdf1[f'{naptan_area_level}'].str.startswith(f'{colvalue}')
        gdf_subframe = gdf1[mask]
        return gdf_subframe

    # expects the full string of the npgt or admin code to work.
    elif naptan_area_level == 'NptgLocalityCode' or 'LocalityName':
        print('This is a locality area.')
        columngroup = gdf.groupby(naptan_area_level)
        gdf_subframe = columngroup.get_group(colvalue)
        gdf_subframe.reset_index(drop=True,
                                 inplace=True)
        return gdf_subframe
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
def get_most_common_value(srs):
    """[summary] gets the most common value within the aac and returns the 
    corresponding most common localities within the Localityname column.
    Arguments:
        srs {[type]} -- [description]
    Returns:
        [counter object] -- [description]
    """
    x = list(srs)
    my_counter = Counter(x)
    return my_counter.most_common(1)[0][0]


# %%
def get_most_common_value_from_field(df,
                                     column_name,
                                     pivot_column='LocalityName'):
    """[summary] Gets the most common value from the field, uses localityname,
    as pivot column. Has been used to get the admin area code to names,
    but may have other uses.

    Args:
        df ([type]): [description]
        columnName ([type]): [description]
        pivot_column (str, optional): [description]. Defaults to 'LocalityName'.

    Returns:
        [type]: [description]
    """

    common_value = df.groupby(f'{column_name}').agg(get_most_common_value)
    common_value_list = common_value[f'{pivot_column}'].tolist()
    common_value.to_csv(f'{column_name}_Most_Common_Counter.csv',
                        usecols=['ATCOCode',
                                 'Geometry'
                                 'LocalityName',
                                 'CommonName',
                                 'AdminAreaCode'])
    print(len(common_value_list))
    return common_value_list


# %%
def get_groupby_admin_area_common_value(df):
    """[summary] uses groupby and aggregation series to get the most locality
    name for each of the admin areas in naptan.

    Arguments:
        df {[type]} -- [description]
    """
    adminAreaGrouping = df.groupby(
                                   ['AdminAreaCode'])['LocalityName'].agg(
                                   pd.Series.mode).to_frame()
    adminAreaGrouping.to_csv('Admin_Area_Codes_Matching.csv',
                             encoding='utf-8')
    return adminAreaGrouping


# %%
def nlp_admin_codes(df):
    """[summary]gets admin codes frequency using nltk, doesn't work quite right.
    """
    nltk.download('stopwords')
    top_N = 152
    stopwords = nltk.corpus.stopwords.words('english')
    # RegEx for stopwords
    RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))
    # replace '|'-->' ' and drop all stopwords
    words = (df.LocalityName
               .str.lower()
               .replace([r'\|', RE_stopwords], [' ', ''], regex=True)
               .str.cat(sep=' ')
               .split())
    # generate DF out of Counter
    rslt = pd.DataFrame(Counter(words).most_common(top_N),
                        columns=['Word', 'Frequency']).set_index('Word')
    print(rslt)

    # plot
    rslt.plot.bar(rot=0, figsize=(16,10), width=0.8)


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
        if naptan_size[0] >= 3000:
            print('This is an admin area.')
        # the below functions should only be run on a locality level or lower
        elif naptan_size[0] <= 300:
            print('This is a locality')
            con.Localities_with_Identical_Stops(gdf)
            geo.road_name_matches_coordinates(gdf)
        # the below functions should only be run on a stop area level or lower
        elif naptan_size[0] <= 30:
            print('This is a stop area.')
            geo.get_nearest_road_name(gdf)
        else:
            print('Naptan Geodata shape is irregular.')
    except Exception as e:
        sys.exit('Given naptan file is too large to process.')
        print(e)

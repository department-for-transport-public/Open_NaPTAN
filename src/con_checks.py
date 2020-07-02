# %%
# testing and Performance
import sys
import os
import re
import timeit
from datetime import datetime
# data wrangling
import pandas as pd
import numpy as np
# docs
# logging
# homebrew
import reporting as report

# %%
# config options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 12)
timestr = datetime.now().strftime("%Y_%m_%d")


# %%
def define_stops_areas(gdf, loc_codes, admin_codes):
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
def detect_nan_values(df, col_name):
    """[summary] Returns the presence of nan values in the naptan dataset.

    Arguments:
        df {[pandas dataframe]} -- [A naptan dataframe.]
        colName {[str]} -- [description]

    Returns:
        [pandas dataframe] -- [a dataframe]
    """
    if df[col_name].isnull().values.any() != 0:
        nan_array = df[col_name].isnull()
        missing_values = df[nan_array]
        percent_missing = df[col_name].isna().sum()/(len(df.Indicator))/100
        print(f'{percent_missing:.4%}')
        df_cleaned = df[missing_values]
        return df_cleaned
    else:
        print('all good.')
        return df


# %%
def remove_illegal_spaces(gdf):
    """[summary] Removes any and all extra spaces they may have been added by
    accident to a naptan field, in the commonname, indicator, street, landmark
    , town, suburb, locality. As we are cleaning data we don't want to report
    back.

    Arguments:
        gdf {[geopandas dataframe]} -- [a pandas dataframe with extra spaces
        involved.]

    Returns:
        [geopandas dataframe] -- [a naptan dataframe with extra spaces removed.]
    """

    check_name = remove_illegal_spaces.__name__
    cols = ['CommonName', 'LocalityName', 'Indicator',
            'Street', 'Landmark', 'Town', 'Suburb']

    for col in cols:
        # the column will sometimes misread as containing floats.
        gdf[col] = gdf[col].astype(str).str.replace('\\D+', '')
        # strip leading and trialing space
        gdf[col] = gdf[col].apply(lambda x: x.strip())
        # remove white space between strings
        gdf[col] = gdf[col].replace('\\s+', ' ', regex=True)
        ris_gdf = gdf
    # if we fix the columns, we don't need to report them, currently.
    # report.nodes_error_reporting(gdf, check_name, ris_gdf)
    print(f'{check_name}, has been completed.')
    return ris_gdf


# %%
def stop_with_multiple_road_names(gdf):
    """[summary]CommonNames in NaPTAN should be simple and not composite. Most
        examples of commonnames which include two of the designated words are
        ones where two road names are used in a composite name, contrary to 
        NaPTAN guidance.
        This uses regex, but they could be some other way of doing this...
    Arguments:
        df {[type]} -- [description]
    """
    check_names = stop_with_multiple_road_names.__name__
    swmrn_gdf = gdf
    swmrn_gdf['CommonName'] = swmrn_gdf['CommonName'].str.lower()

    # leave this here, no it's not being used, just leave it anyway.
    targets = ['road', 'roads',
               'street', 'streets',
               'avenue', 'avenues',
               'garden', 'gardens',
               'lane', 'lanes',
               'drive', 'drives',
               'way', 'ways']

    pattern = (r"\b(road|roads|\
                    street|streets|\
                    avenue|\avenues|\
                    garden|gardens|\
                    lane|lanes\
                    drive|drives\
                    way|ways)\b")

    fail_rds_re = (r"\b('street|streets|avenue|avenues|garden|"
                   r"gardens|lane|lanes|drive|drives|way|ways')\b")
    fail_aves_re = (r"\b('road|roads|street|streets|garden|gardens|"
                    r"lane|lanes|drive|drives|way|ways')\b")
    fail_gdns_re = (r"\b('road|roads|street|streets|avenue|avenues|"
                    r"lane|lanes|drive|drives|way|ways')\b")
    fail_lanes_re = (r"\b('road|roads|street|streets|avenue|avenues|"
                     r"garden|gardens|drive|drives|way|ways')\b")
    fail_drives_re = (r"\b('road|roads|street|streets|avenue|avenues|"
                      r"garden|gardens|lane|lanes|way|ways')\b")
    fail_ways_re = (r"\b('road|roads|street|streets|avenue|avenues|"
                    r"garden|gardens|lane|lanes|drive|drives')\b")

    tn = swmrn_gdf[swmrn_gdf['CommonName'].str.contains(pattern,
                                                        regex=True)]
    roads = tn[tn['CommonName'].str.contains(r"\b(road|roads)\b")]
    fail_rds = roads[roads['CommonName'].str.contains(fail_rds_re,
                                                      regex=True)]
    aves = tn[tn['CommonName'].str.contains(r"\b(avenue|avenues)\b")]
    fail_aves = aves[aves['CommonName'].str.contains(fail_aves_re,
                                                     regex=True)]
    gdns = tn[tn['CommonName'].str.contains(r"\b(garden|gardens)\b")]
    failgdns = gdns[gdns['CommonName'].str.contains(fail_gdns_re,
                                                    regex=True)]
    lanes = tn[tn['CommonName'].str.contains(r"\b(lane|lanes)\b")]
    faillanes = lanes[lanes['CommonName'].str.contains(fail_lanes_re,
                                                       regex=True)]
    drives = tn[tn['CommonName'].str.contains(r"\b(drive|drives)\b")]
    faildrives = drives[drives['CommonName'].str.contains(fail_drives_re,
                                                          regex=True)]
    ways = tn[tn['CommonName'].str.contains(r"\b(way|ways)\b")]
    failways = ways[ways['CommonName'].str.contains(fail_ways_re,
                                                    regex=True)]
    all_dfs = [fail_rds, fail_aves, failgdns,
               faillanes, faildrives, failways]
    failed_nodes = pd.concat(all_dfs)
    failed_nodes['CommonName'] = failed_nodes['CommonName'].str.title()
    report.nodes_error_reporting(gdf, check_names, failed_nodes)
    return failed_nodes


# %%
def node_has_repeating_word(gdf):
    """[summary]

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = node_has_repeating_word.__name__
    gdf1 = gdf[['ATCOCode',
                'CommonName',
                'LocalityName',
                'Indicator']].apply(lambda x: ' '.join(x.astype(str)),
                                    axis=1)
    split = gdf1['CommonName'].str.split(expand=True)
    split1 = gdf1['LocalityName'].str.split(expand=True)
    split2 = gdf1['Indicator'].str.split(expand=True)
    gdf2 = pd.concat([split, split1, split2],
                     axis=1,
                     ignore_index=True)
    raise NotImplementedError


# %%
def node_repeating_word(df):
    """[summary] StopPoint has a full name [Locality, CommonName (Indicator)]
    containing three or more occurrences of any single word.
    There is a standard minimum content for the unique identification of stops
    in downstream systems – which comprises “Locality (without qualifier),
    Common Name (indicator)”.
    Downstream systems using the data do not want unnecessary duplication of
    words within this formulation of stop names (on timetables, for instance)
    this test identifies situations in which the same word appears three or
    more times in the concatenated stopname.

    Arguments:
        df {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    check_name = Node_Has_Repeating_Word.__name__
    df1 = df[['ATCOCode', 'CommonName', 'LocalityName', 'Indicator']]
    spec_chars = ["!", '"', "#", "%", "&", "'", "(", ")",
                  "*", "+", ",", "-", ".", "/", ":", ";", "<",
                  "=", ">", "?", "@", "[", "\\", "]", "^", "_",
                  "`", "{", "|", "}", "~", "–"]
    for char in spec_chars:
        df1['CommonName'] = df1['CommonName'].str.replace(char, ' ')
    split = df1['CommonName'].str.split(expand=True)
    split1 = df1['LocalityName'].str.split(expand=True)
    split2 = df1['Indicator'].str.split(expand=True)
    df2 = pd.concat([split, split1, split2],
                    axis=1,
                    ignore_index=True)

    df3 = (df2.fillna('')
            .groupby(df2.columns.tolist()).apply(len)
            .rename('Repeat_Count')
            .replace('',np.nan)
            .sort_values(by= ['Repeat_Count'], ascending=False))
    mask = (df3['Repeat_Count'] > 2) #  TODO this works but can't be assigned,
    # back to the original data frame for boolean indexing
    return mask
    raise NotImplementedError
    print('Not implemented at this time.')


# %%
def remove_illegal_chars(gdf, col_name):
    """[summary - removes illlegal characters from the given Naptan stops file.

    Arguments:
        gdf {[geopandas dataframe]} -- [the naptan master dataframe]
        columnName {[str]} -- [a given column name to search through]
    Returns:
        df -- a df object that has had illegal characters removed, from the
        given field.
    """

    # for reporting
    check_name = remove_illegal_chars.__name__
    gdf1 = gdf
    # our regex pattern of allowed special characters.
    pattern = r"\bO/S|NO\.|P\.H\.|P\.O\.|ST\.|'s\b"
    excluded_nodes = gdf1[gdf1[col_name].str.contains(pattern,
                                                      case=False,
                                                      regex=True)]
    mask = gdf1[col_name].isin(excluded_nodes[col_name])
    df_filter = gdf1[~mask]  # removing excluded nodes from stops frame.
    regex = re.compile(r"\[^a-zA-Z !@#$%&\*_\+=\|:;<>,./[\]\{\}\']",
                       flags=re.IGNORECASE)
    df_filter[col_name] = df_filter[col_name].str.replace(regex,
                                                          '',
                                                          regex=True)
    report.nodes_error_reporting(gdf, check_name, df_filter)
    result = df_filter.append(excluded_nodes)
    return result


# %%
def stop_with_bearing_missing(gdf):
    """[summary] The data does not include a value for “bearing” for all BCT
     stops except those in the FLX (flexible zone) sub-type.

    Args:
        gdf {[geopandas dataframe]} -- [The naptan master dataframe.]

    Returns:
        [type]: [description]
    """
    check_name = stop_with_bearing_missing.__name__
    valid_bearing = ['SW', 'NE', 'SE', 'S', 'N', 'NW', 'E', 'W']
    failed_nodes = gdf[(gdf['StopType'] == 'BCT') &
                       (gdf['BusStopType'] != 'FLX') &
                       (~gdf['Bearing'].isin(valid_bearing))]
    report.nodes_error_reporting(gdf,
                                 check_name,
                                 failed_nodes)
    return failed_nodes


# %%
def stop_name_contains_locality_name(gdf):
    """[summary]- When stop names are presented in public information systems
        they are generally shown with the locality. If the CommonName also
        includes the name of the locality, then the result is duplication in
        the concatenated stopname, which makes the name longer than is
        necessary. However, there are situations where the name of the stop
        legitimately will include the locality name – such as “Rugby School”
        – because “Rugby, School” could refer to any one of many schools,
        only one of which is “Rugby School”.

    Arguments:
        gdf {[geopandas dataframe]} -- [the naptan master dataframe]

    Returns:
        [geopanads dataframe] -- [a list of all stops where the common name and
        locality name, match exactly and no excluding terms are found to excuse
        this, there should be a set number of them but if that number
        increases, this should be addressed.]
    """

    check_name = stop_name_contains_locality_name.__name__
    try:
        df = gdf[['ATCOCode', 'CommonName', 'LocalityName']]
        cn, ln = df['CommonName'], df['LocalityName']
        cnsum, lnsum = cn.isnull().sum(), ln.isnull().sum()
        # permitted terms to include
        terms = ['Academy', 'Arms', 'Avenue', 'Bridge', 'Centre',
                 'Church', 'Close', 'Club House', 'College', 'Common',
                 'Corner', 'Cottages', 'Crescent', 'Cross Roads',
                 'Cross', 'Crossroads', 'Dock', 'Drive', 'Estate',
                 'Farm', 'Ferry', 'Gardens', 'Green', 'Hall',
                 'Health Centre', 'Hill', 'Hospital', 'Hotel',
                 'House', 'Hoverport', 'Industrial Area', 'Inn',
                 'Island', 'Junction', 'Landing', 'Lane', 'Lodge',
                 'Main Street', 'Manor', 'Metrolink', 'Mill', 'Park',
                 'Pier', 'Place', 'Post Office', 'Rail', 'Railway',
                 'Rd', 'Road', 'Roundabout', 'School', 'Square',
                 'Station', 'Street', 'Supertram', 'Terminal',
                 'Terrace', 'Tramlink', 'Tramway', 'Turn',
                 'Underground', 'Village', 'Way']

        if cnsum or lnsum != 0:
            errors = ('Column entries contain null entries check automatically\
                fails.')
            return errors

        else:
            df_com = [df[0] in df[1] for df in zip(df['CommonName'],
                      df['LocalityName'])]
            colvalues = pd.Series(df_com)
            df.insert(loc=0, column='NameMatch', value=colvalues)
            mns = df[df['NameMatch']]
            mns = mns.drop(['NameMatch'], axis=1)
            # we create a mask to identify an excluded terms occuring in the
            #  remain duplicates, that should be ignored. We do this for both the
            #  Common name and Localityname, column.
            cn_mask = np.logical_or.reduce([mns['CommonName'].str.contains(t,
                                           regex=False,
                                           case=False) for t in terms])
            mns = mns[cn_mask]
            ln_mask = np.logical_or.reduce([mns['LocalityName'].str.contains(t,
                                           regex=False,
                                           case=False) for t in terms])
            mns = mns[ln_mask]
            # reports returns percentage of bad stops out of all stsops,
            #  about 0.03%
            report.nodes_error_reporting(gdf, check_name, mns)
            return mns

    except ValueError as ve:
        # ValueError: Cannot mask with non-boolean array containing NA /
        #  NaN values
        # sys.exit(f'{ve}')
        pass


# %%
def check_name_too_long(gdf):
    """[summary]:- A stop point fails if StopPoint has a full name [Locality,
     CommonName (Indicator)] that is more than 80 characters in length.

    Arguments:
        gdf {[geopandas dataframe]} -- [The naptan master dataframe.]
    Returns:
        df {[dataframe of failed nodes]} -- Nodes that failed the check.
    """
    check_name = check_name_too_long.__name__
    gdf1 = gdf
    gdf1['newName'] = gdf1['CommonName'].astype(str) + ', ' + gdf1['LocalityName'].astype(str)
    mask = (gdf1['newName'].str.len() > 80)
    df_str = gdf1.loc[mask]
    report.nodes_error_reporting(gdf, check_name, df_str)
    return df_str.ATCOCode


# %%
def stop_names_with_high_risk_words(gdf):
    """[summary] Descriptions: StopPoint has a CommonName that contains one of
     the following high risk words: DELETE, DELETED, N/A, N/K, OBSOLETE,
        UNUSED (case-insensitive).
    Args:
        gdf ([geopandas ]): [a pandas dataframe of the current naptan file.]

    Returns:
        df_risks [type]: [csv file containing risk updates.]
    """

    check_name = stop_names_with_high_risk_words.__name__
    gdf1 = gdf
    riskwords = ['DELETE', 'DELETED', 'N/A', 'NOT IN USE'
                 'N/K', 'OBSOLETE', 'UNUSED']
    gdf1['CommonName'] = gdf1['CommonName'].str.upper()
    gdf1['RiskWords'] = gdf1['CommonName'].apply(
        lambda x: 1 if any(i in x for i in riskwords) else 0)
    df_risks = gdf1.loc[gdf1['RiskWords'] != 0]
    endcol = len(df_risks.columns)
    df_risks.insert(endcol, 'Warning Flag', check_name)
    report.nodes_error_reporting(gdf, check_name, df_risks)
    return df_risks
    # TODO indicate if it's a bus stop, if so flag locality or authorities
    #  that should confirm the stops deletion from the database.


# %%
def remove_illegal_caps(gdf, column_name):
    """[summary] Descriptions:CommonNames should not contain acronyms as single capitals
        separated by spaces or full stops – with the exception of „R C‟,
        „P.H.‟, and „P.O.‟. CommonNames should not contain a sequence
        of lowercase letter followed by uppercase letter – with the
        exceptions of 'McX' and 'MacX'
    Args:
        gdf ([pandas dataframe]): [the master naptan nodes file.]
        columnName ([type]): [description]

    Returns:
        IIC [type]: [description]
    """

    check_name = remove_illegal_caps.__name__
    gdf1 = gdf
    except_caps = ['AFC', 'ASDA', 'BBC', 'BP', 'CE', 'DHSS', 'DLR',
                   'FC', 'GMEX', 'HMP', 'HQ', 'HSBC', 'II', 'III',
                   'IKEA', 'IV', 'IX', 'MFI', 'MOD', 'NCP', 'NE', 'NR',
                   'NW', 'PH', 'PO', 'RAF', 'RC', 'RSPCA', 'SE', 'SPT',
                   'SW', 'VI', 'VII', 'VIII', 'WMC', 'XI', 'XII',
                   'YMCA', 'YWCA']
    gdf1['capitals'] = gdf1[column_name].str.count('[A-Z]{3,}')
    gdf1 = gdf1[gdf1['capitals'] != 0]
    # the below, compares a list against named column
    mask = ~gdf1[column_name].apply(lambda x: np.intersect1d(x,
                                                             except_caps).size > 0)
    iic = gdf1[mask]
    report.nodes_error_reporting(gdf, check_name, iic)
    return iic


# %%
def localities_with_identical_stops(gdf_locality):
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
    check_name = localities_with_identical_stops.__name__
    gdf1 = gdf_locality
    try:
        if len(gdf1['NptgLocalityCode'].unique()) == 1:
            mask = gdf1['StopPoint'].duplicated()
            failed_nodes = gdf1[mask]
            report.nodes_error_reporting(gdf_locality,
                                         check_name,
                                         failed_nodes)
            return failed_nodes

    except Exception as e:
        print(f'Not a locality, test can not be performed. {e}')
        pass


# %%
def stops_in_different_admin_area(gdf):
    """[summary] Checks if a stop is in a different administrative area, based
    on the AtcoAreaCode Column. We take the first 3 characters prefix of the 
    atcocode and check them against the atcoareacode for the admin area.
    They should match.
    Args:
        gdf ([pandas dataframe]): [The Master naptan node frame.]
    Returns:
        [panda dataframe] -- [description]
    Raises:
        NotImplementedError: [geo spatial cross checking, not implemented yet.]
    """
    check_name = stops_in_different_admin_area.__name__
    gdf1 = gdf
    #  get prefix from atcocode column
    gdf1['atcocodeprefix'] = gdf1['ATCOCode'].str[:3]
    #  get the AtcoAreaCode column value, making sure that we account for 
    # 2-digit atcocode prefixes and int types, using to_numeric
    gdf1['AtcoAreaCode'] = gdf1['AtcoAreaCode'].astype(str)
    gdf1['atcocodeprefix'] = pd.to_numeric(gdf1['atcocodeprefix'])
    gdf1['AtcoAreaCode'] = pd.to_numeric(gdf1['AtcoAreaCode'])
    #  compare the two together, they should match
    gdf1['not matching'] = gdf1['atcocodeprefix'].eq(pd.to_numeric(
                          gdf1['AtcoAreaCode'], errors='coerce'))
    failed_nodes = gdf1[~gdf1['not matching']]
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError
    # TODO if they don't match, report the nodes that don't match
    # TODO compare the geometry point to the polygon boundaries of the expected
    #  admin area
    # TODO if the geometry point is further 500 meters outside the boundaries
    #  of the given area, then the node fails


# %%
def stops_area_members_without_identical_names(gdf):
    """[summary]

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = stops_area_members_without_identical_names.__name__
    gdf1 = gdf
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def stops_in_alternate_localities(gdf):
    """[summary]

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = stops_in_alternate_localities.__name__
    gdf1 = gdf
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError


# %%
def locality_not_unique(gdf):
    """[summary]

    Args:
        gdf ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    check_name = locality_not_unique.__name__
    gdf1 = gdf
    failed_nodes = ''
    report.nodes_error_reporting(gdf, check_name, failed_nodes)
    return failed_nodes
    raise NotImplementedError

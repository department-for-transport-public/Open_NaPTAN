import pandas as pd
from report.reporting import write_basic_log_file, report_failing_nodes

# %%


def detect_nan_values(gdf, col_name):
    """[summary] This is an internal open naptan method, it shouldn't be exposed
    to the user unless required for reporting widespread data issues.
    Returns the presence of nan values in the naptan dataset for
    a given column.
    Arguments:
        gdf {[pandas dataframe]} -- [A naptan dataframe.]
        colName {[str]} -- [a column str name as expected in the naptan data
        column.]

    Returns:
        [pandas dataframe] -- [a dataframe]
    """
    # nodes into a report ,
    check_name = 'Required columns contain null values.'
    # the below list is columns which must
    required_cols = ['ATCOCode', 'CommonName', 'Street', 'Indicator',
                     'Bearing', 'NptgLocalityCode', 'Town', 'TownLang',
                     'Suburb', 'LocalityCentre', 'Longitude', 'Latitude',
                     'StopType', 'BusStopType', 'TimingStatus', 'AdminCode',
                     'CreationDateTime', 'ModificationDateTime', 'Status',
                     'StopPoint', 'LocalityName', 'QualifierName',
                     'AtcoAreaCode', 'AreaName', 'RegionCode',
                     'Status_area', 'geometry']
    # check if the column is a required column. Defensive.
    if col_name not in required_cols:
        message = f'{col_name} for the area {gdf.AreaName.iloc[0]} the \
        requested column can have null values. This '
        write_basic_log_file(message)
        pass
    # Check is the column contains any null or na values.
    elif gdf[col_name].isnull().values.any() != 0:
        nan_array = gdf[col_name].isnull()
        # build array of missing values, using masking.
        missing_values = gdf[nan_array]
        percent_missing = gdf[col_name].isna().sum()/(len(gdf.Indicator))/100
        # return missing percentage of rows.
        print(f'{percent_missing:.4%}')
        df_cleaned = gdf[missing_values]
        report_failing_nodes(gdf, test_name=check_name,
                             failed_nodes=missing_values)
        return df_cleaned
    else:
        message = f'{col_name} for the area {gdf.AreaName.iloc[0]} has missing \
        values in a required column and has failed this test.'
        print('all good.')
        pass

# %%
import pandas as pd
import numpy as np
import faker
from hypothesis.strategies import text
from hypothesis import given, example
import faker.providers.geo


class FakeNaptanGenerator(faker):
    """[summary]

    Args:
        faker ([type]): [description]
    """
    # create fake UK localised data
    fake = faker('en_UK')

    def fake_naptan_(df, colname, insertString):
        """[summary]  this function is for creating fake naptan data.

        Arguments:
            df {[type]} -- [description]
            colname {[type]} -- [description]
            insertString {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        df = pd.Series(['ATCOCode',
                        'NaptanCode', 'PlateCode', 'CleardownCode',
                        'CommonName',
                        'CommonNameLang', 'ShortCommonName', 'ShortCommonNameLang',
                        'Landmark',
                        'LandmarkLang', 'Street', 'StreetLang', 'Crossing',
                        'CrossingLang',
                        'Indicator', 'IndicatorLang', 'Bearing',
                        'NptgLocalityCode',
                        'LocalityName', 'ParentLocalityName',
                        'GrandParentLocalityName', 'Town',
                        'TownLang', 'Suburb', 'SuburbLang', 'LocalityCentre',
                        'GridType',
                        'Easting', 'Northing', 'Longitude', 'Latitude', 'StopType',
                        'BusStopType', 'TimingStatus', 'DefaultWaitTime', 'Notes',
                        'NotesLang',
                        'AdministrativeAreaCode', 'CreationDateTime',
                        'ModificationDateTime',
                        'RevisionNumber', 'Modification', 'Status'])
        return df

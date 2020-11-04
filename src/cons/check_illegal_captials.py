import numpy as np
from report.reporting import report_failing_nodes

from src.checks import NaptanCheck

# %%


class IllegalCaptials(NaptanCheck):
    """[summary] A collection of methods for dealing with the presence of 
    illegal capitals in the naptan dataset.

    Args:
        NaptanCheck ([type]): [description]
    """
    # for reporting
    check_name = 'Check Illegal Capitals'
    check_warning_level = 'low'
    check_geographic_level = 'stop'

    @classmethod
    def check_illegal_caps(cls, gdf, col_name='StopPoint'):
        """[summary] Descriptions:CommonNames should not contain acronyms as single
            capitals separated by spaces or full stops – with the exception of
            „R C‟, „P.H.‟, and „P.O.‟. CommonNames should not contain a sequence
            of lowercase letter followed by uppercase letter – with the
            exceptions of 'McX' and 'MacX'
        Args:
            gdf ([pandas dataframe]): [the master naptan nodes file.]
            columnName ([type]): [description]

        Returns:
            IIC [type]: [description]
        """

        except_caps = ['AFC', 'ASDA', 'BBC', 'BP', 'CE', 'DHSS', 'DLR',
                       'FC', 'GMEX', 'HMP', 'HQ', 'HSBC', 'II', 'III',
                       'IKEA', 'IV', 'IX', 'MFI', 'MOD', 'NCP', 'NE', 'NR',
                       'NW', 'PH', 'PO', 'RAF', 'RC', 'RSPCA', 'SE', 'SPT',
                       'SW', 'VI', 'VII', 'VIII', 'WMC', 'XI', 'XII',
                       'YMCA', 'YWCA']
        try:
            # clone
            gdf1 = gdf
            gdf1['capitals'] = gdf1[col_name].str.count('[A-Z]{3,}')
            gdf1 = gdf1[gdf1['capitals'] != 0]
            # the below, compares a list against named column
            mask = ~gdf1[col_name].apply(
                lambda x: np.intersect1d(x, except_caps).size > 0)
            # masking if required.
            illegal_caps = gdf1[mask]
            # save the report.
            report_failing_nodes(
                gdf, 'Check illegal capitals', illegal_caps)
            print('Illegal Captials has completed.')
            return illegal_caps
        except Exception as e:
            print(f'{e}')
        except ValueError as ve:
            print(f'{ve}')

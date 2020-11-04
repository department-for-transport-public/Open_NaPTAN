import pytest
from cons.check_datetime import check_datetime
import pandas as pd

from datetime import datetime


test_data = pd.DataFrame(
    {
        "0": ["a", "b", "c"],
        "ModificationDateTime": [
            pd.Timestamp("2020-11-03"),
            ("2020-11-04"),
            ("2030-12-29"),
        ],
        "2": [11, 12, 13],
    }
)

check_datetime(test_data)
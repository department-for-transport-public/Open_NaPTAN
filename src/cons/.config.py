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
import report.reporting as report
import visualise.visualiser as vis
import etl.etl_pipe as etl

# %%
# config options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
timestr = datetime.now().strftime("%Y_%m_%d")


#

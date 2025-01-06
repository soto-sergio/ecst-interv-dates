# Import packages and files
import os
import sys
from ecst_func import *
from pipeline.report_processing import *



#### To convert it as exe
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#### Path
path = os.getcwd()
path = path.replace('\\','/')

#### Pre-processing data
## Call function report_preprocessing() to transform and clean the data from xlsx to csv and saves it as data/clean/hr_clean.csv
report_preprocessing()   # w?y Only to be run after downloading the Report xlsx file.

## Call function csv_to_dict() to save csv as dictionary using pickle  
dict_saved =csv_to_dict(path + "/data/clean/homeroom_clean.csv", key_col = 0, value_col=1)   #w?y
## Call dictionary using pickle
dict_callback = load_dict(path + "/data/clean/hr_dict.pkl")  #w?y

## Send dict_callback to a function
get_dict(dict_callback)

## Call GUI frames
tk_root()

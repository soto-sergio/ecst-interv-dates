## Import libraries and packages
import pandas as pd
import os
import warnings

def report_preprocessing():
    ## Ignore warnings style of the csv file
    warnings.filterwarnings("ignore", category=UserWarning, message="Workbook contains no default style, apply openpyxl's default")

    ## Save Report into data/raw folder with default name: ClassStudentListingwithAddresses

    ## Path to xlsx file
    parent_dir = os.path.join(os.path.dirname(__file__))
    grandparent_dir = os.path.join(os.path.dirname(parent_dir))
    data_path = os.path.join(grandparent_dir, 'data\\raw', 'ClassStudentListingwithAddresses.xlsx')
    data_path = data_path.replace('\\','/')
    read_xl = pd.read_excel(data_path)

    ## Save xlsx to csv
    grandparent_dir = grandparent_dir.replace('\\','/')
    read_xl.to_csv(grandparent_dir + "/data/processed/homeroom_raw.csv")

    ## Open csv file
    df = pd.read_csv(grandparent_dir + "/data/processed/homeroom_raw.csv" )

    ## Drop unnecessary rows
    df = df.drop([0])  # Drop rows
    df = df.iloc[:, [4 ,5]]

    ## Raneme columns
    df= df.rename(columns = {
        'Unnamed: 3' : 'student_name', 
        'Unnamed: 4' : 'student_id'})
    ## Rearrange order of columns
    df = df[['student_id', 'student_name']]
    
    ## Change type of data
    df["student_id"] = df["student_id"].astype(int)
    df["student_name"] = df["student_name"].astype(str)         
    
    ## Save final csv file
    df.to_csv(grandparent_dir + "/data/clean/homeroom_clean.csv", index = None, header=None)

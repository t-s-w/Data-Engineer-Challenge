from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
import pandas as pd
import re
from datetime import datetime
import os
from hashlib import sha256
import logging

os.chdir('/home/amph/')

input_path = './input/'
output_success_path = './output/success/'
output_fail_path = './output/fail/'
date_columns = ['date_of_birth']

def name_check(name):
    # Supporting function to check validity of Name. Since missing names will be read as NaN in pandas, the name != name is used to check for missing names.
    # Afterwards, a name is valid only if it's not just whitespace, and if it is a full name (not just one name).
    if name != name: 
        return False
    split = name.split(' ')
    return True if sum([len(x) for x in split]) > 0 and len(split) > 1 else False

def email_check(email):
    # Supporting function to check validity of email. Same NaN check applies. There could be emails other than .com or .net email providers,
    # but since the challenge specifically states .com or .net only I will take that to be a business requirement.
    if email != email:
        return False
    return re.search('@[a-zA-Z-]+.(com|net)$',email) is not None

def extract_hash(YYYYMMDD):
    # Extract first five bytes from SHA256 hash of YYYYMMDD-form birthday.
    return sha256(YYYYMMDD.encode('utf-8')).hexdigest()[0:5]


def extract_names(name,index):
    #E xtract first name and last name from name.
    split = name.split(' ')
    return split[index]

def load_data():
    # Function to read and process the data while splitting it into successful/unsuccessful in DAG. Mobile numbers tend to be read in as numbers, so convert to str
    datafiles = [input_path + file for file in os.listdir(input_path) if re.search('^applications_dataset_.*\.csv$',file) is not None]
    df = pd.concat(map(pd.read_csv,datafiles))
    df.reset_index(drop=True,inplace=True)
    df['mobile_no'] = df['mobile_no'].apply(str)
    # date_of_birth column is very dirty and has different formats, but they seem to consistently be interpretable by pandas.to_datetime (i.e. either yyyy/mm/dd, dd/mm/yyyy, dd-mm-yyyy, yyyy-mm-dd)
    # there are some invalid dates (there was a 31st feb associated to a Lori Torres), but these will be coerced to NaT and filtered by the next tests.
    # as for dd/mm/yyyy vs mm/dd/yyyy, sometimes there's just no way to know, so just take the default which is mm/dd/yyyy.
    df['date_of_birth'] = df['date_of_birth'].apply(pd.to_datetime,errors='coerce')
    # Check for mobile number length, age, non-empty name, and valid email, then define successful applications to be the ones that passed all these tests
    df['mobile_length_check'] = df['mobile_no'].apply(lambda x: len(x) == 8)
    df['above_18'] = df['date_of_birth'].apply(lambda x: (2022 - x.year) >= 18)
    df['name_check'] = df['name'].apply(name_check)
    df['email_check'] = df['email'].apply(email_check)
    success = df['mobile_length_check'] & df['above_18'] & df['name_check'] & df['email_check']
    # Split entries into successful and unsuccessful
    successful_apps = df.loc[success,['name','date_of_birth','email','mobile_no','above_18']]
    unsuccessful_apps = df.loc[~success]

    # write out the unsuccessful entries into the output/fail/ folder along with the checks to show why they failed
    unsuccessful_apps.to_csv(output_fail_path+'Failed_Ingest_'+datetime.now().strftime('%Y-%m-%d-%H%M')+'.csv', index=False)

    # Perform the requested transformations on the successful entries
    successful_apps['date_of_birth'] = df['date_of_birth'].dt.strftime('%Y%m%d')
    successful_apps['first_name'],successful_apps['last_name'] = successful_apps['name'].apply(extract_names,index=0), successful_apps['name'].apply(extract_names,index=1)
    successful_apps['ID'] = successful_apps['last_name'] + '_' + successful_apps['date_of_birth'].apply(extract_hash)

    # write out the successful entries to output/success/ folder
    successful_apps = successful_apps.loc[:,['first_name','last_name','email','date_of_birth','ID','above_18']]
    successful_apps.to_csv(output_success_path + 'Processed_'+datetime.now().strftime('%Y-%m-%d-%H%M')+'.csv', index=False)

    # Delete the processed ingestion file
    for file in [input_path + file for file in os.listdir(input_path) if re.search('^applications_dataset_.*\.csv$',file) is not None]:
        os.remove(file)
        

with DAG("application_pipeline", # Dag id
start_date=datetime(2023, 4 ,13), # start date, the 1st of January 2021 
schedule_interval='@hourly',  # Cron expression, here it is a preset of Airflow, @daily means once every day.
catchup=False  # Catchup 
) as dag:
    task_1 = PythonOperator(
    task_id='load_data',
    python_callable = load_data,
    dag = dag
    )
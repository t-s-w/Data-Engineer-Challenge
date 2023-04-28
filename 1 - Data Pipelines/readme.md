# Section 1 - Data Pipelines

## Problem Statement


An e-commerce company requires that users sign up for a membership on the website in order to purchase a product from the platform. As a data engineer under this company, you are tasked with designing and implementing a pipeline to process the membership applications submitted by users on an hourly interval.

Applications are batched into a varying number of datasets and dropped into a folder on an hourly basis. You are required to set up a pipeline to ingest, clean, perform validity checks, and create membership IDs for successful applications. An application is successful if:

* Application mobile number is 8 digits
* Applicant is over 18 years old as of 1 Jan 2022
* Applicant has a valid email (email ends with @emailprovider.com or @emailprovider.net)

You are required to format datasets in the following manner:

* Split name into first_name and last_name
* Format birthday field into YYYYMMDD
* Remove any rows which do not have a name field (treat this as unsuccessful applications)
* Create a new field named above_18 based on the applicant's birthday
* Membership IDs for successful applications should be the user's last name, followed by a SHA256 hash of the applicant's birthday, truncated to first 5 digits of hash (i.e <last_name>_<hash(YYYYMMDD)>)

You are required to consolidate these datasets and output the successful applications into a folder, which will be picked up by downstream engineers. Unsuccessful applications should be condolidated and dropped into a separate folder.

You can use common scheduling solutions such as cron or airflow to implement the scheduling component. Please provide a markdown file as documentation.

## Solution Explanation

`DAG.py` is a DAG file that can be used in an Apache Airflow implementation. The following parameters are used:

* `AIRFLOW_HOME` was set to `~/airflow`.
* The working directory of the DAG was set to `/home/amph/` in the DAG. File input location is `/home/amph/input`, and output folders are `home/amph/output/fail` and `home/amph/output/success`.

The DAG was tested until it ran successfully, which would be indicated by the input files being deleted and the output files showing up in the respective folders. The output files were then extracted from the WSL file system and added to this repo.

## DAG Details

The DAG will take data from the ingestion folder, `/home/amph/input`. It will accept only `.csv` files with names that follow the pattern `applications_dataset_[ ].csv` where content in the brackets can be numbers or empty, similar to the files given.

Correct formatting, column names, etc is assumed to be similar to the given test data files.

The DAG will ingest all data simultaneously and concatenate all of the loaded datasets into a larger dataframe, then perform processing

For each of the rules given, the DAG will create a new column in the DataFrame:

* `mobile_length_check` is `True` if `mobile_no` is exactly 8 characters long and `False` otherwise.
* `above_18` checks whether the age of the person as of 1 Jan 2022 is at least 18 years old.
* `name_check` checks that a first and last name can be retrieved from the name, after checking for empty names.
* `email_check` checks that the email corresponds to a @emailprovider.com or @emailprovider.net email as given in the requirements. @emailprovider.biz and .org emails are excluded, along with other kinds of domains.

If all of these is `True`, then a row will get included in a `successful_apps` dataframe; else they will be diverted into a `unsuccessful_apps` dataframe.

The `unsuccessful_apps` data frame will be out put into the `output/fail` folder with the check columns to explain why a particular application was rejected for debugging purposes.

The `successful_apps` dataframe will have the other required transformations performed on it, then output into a csv file in the `output/success` folder which can be picked up by downstream engineers.

At the end, the input files will be deleted to avoid double-creation of records.
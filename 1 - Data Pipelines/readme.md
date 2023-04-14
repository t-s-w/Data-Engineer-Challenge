# Section 1 - Data Pipelines

I am normally a Windows user, so I had to look up a guide to use WSL to launch Airflow. The DAG was tested in Airflow, with specific hard-coded locations for the environment (due to my unfamiliarity with WSL):

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
# Section 1 - Data Pipelines

I am normally a Windows user, so I had to look up a guide to use WSL to launch Airflow. The DAG was tested in Airflow, with specific hard-coded locations for the environment (due to my unfamiliarity with WSL):

* `AIRFLOW_HOME` was set to `~/airflow`.
* The working directory of the DAG was set to `/home/amph/` in the DAG. File input location is `/home/amph/input`, and output folders are `home/amph/output/fail` and `home/amph/output/success`.

The DAG was tested until it ran successfully, which would be indicated by the input files being deleted and the output files showing up in the respective folders. The output files were then extracted from the WSL file system and added to this repo.

How the DAG works is outlined in the comments of `DAG.py`.
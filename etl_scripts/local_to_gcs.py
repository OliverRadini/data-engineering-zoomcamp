from google.cloud import storage
from util.authenticate_gcp import authenticate_gcp
from util.write_to_gcs import write_to_gcs

authenticate_gcp("sturdy-ranger-384021")

def local_to_gcs(file_location, contents):
    PROJECT_NAME = "dtc_data_lake_sturdy-ranger-384021"
    write_to_gcs(PROJECT_NAME, f"data/{file_location}", contents)

local_to_gcs("test/one.md", "## hello, world")
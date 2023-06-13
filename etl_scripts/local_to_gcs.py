from google.cloud import storage
from util.authenticate_gcp import authenticate_gcp
from util.write_to_gcs import write_to_gcs

BUCKET_NAME = "dtc_data_lake_sturdy-ranger-384021"
PROJECT_NAME = "sturdy-ranger-384021"

# TODO: make this work with command line arguments

def local_to_gcs(file_location, contents):
    write_to_gcs(BUCKET_NAME, f"data/{file_location}", contents)

authenticate_gcp(PROJECT_NAME)

local_to_gcs("test/one.md", "## hello, world")
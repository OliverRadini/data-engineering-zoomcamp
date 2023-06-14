import argparse
from google.cloud import storage
from util.authenticate_gcp import authenticate_gcp
from util.write_to_gcs import write_to_gcs

BUCKET_NAME = "dtc_data_lake_sturdy-ranger-384021"
PROJECT_NAME = "sturdy-ranger-384021"

parser = argparse.ArgumentParser()

parser.add_argument("--file")
parser.add_argument("--bucket")

args = parser.parse_args()

authenticate_gcp(PROJECT_NAME)

def local_to_gcs(file_location, contents):
    write_to_gcs(BUCKET_NAME, f"data/{file_location}", contents)

print("About to read file...")

with open(args.file) as f:
    print("File read, writing to GCS...")
    local_to_gcs(args.bucket, f.read())
    print("Done")

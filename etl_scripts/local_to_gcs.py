import argparse
import pandas as pd
from google.cloud import storage
from util.authenticate_gcp import authenticate_gcp
from util.write_to_gcs import write_to_gcs

BUCKET_NAME = "dtc_data_lake_sturdy-ranger-384021"
PROJECT_NAME = "sturdy-ranger-384021"

parser = argparse.ArgumentParser()

parser.add_argument("--color")
parser.add_argument("--year")
parser.add_argument("--month")

args = parser.parse_args()

authenticate_gcp(PROJECT_NAME)

month = args.month.zfill(2);
file_name = f"{args.color}_tripdata_{args.year}-{month}.csv"
local_location = f"./data/{args.color}/{file_name}"

print(f"About to read file from {local_location}...")

df = pd.read_csv(local_location, compression="gzip")

df.to_csv(f"gs://{BUCKET_NAME}/data/{args.color}/{file_name}")

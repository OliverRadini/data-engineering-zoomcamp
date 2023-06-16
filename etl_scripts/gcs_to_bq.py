from google.cloud import bigquery
import argparse

from util.parse_standard_args import parse_standard_args

PROJECT_NAME = "sturdy-ranger-384021"
DATASET = "dezoomcamp"
FILE_ROOT = f"gs://dtc_data_lake_sturdy-ranger-384021/data/"

args = parse_standard_args()

table_name = "rides"

month = args.month.zfill(2);
file_location = f"{FILE_ROOT}{args.color}/{args.color}_tripdata_{args.year}-{month}.csv"

# establish a client for communicating with big query
client = bigquery.Client()

# the identity of the table to write to
table_id = f"{PROJECT_NAME}.{DATASET}.{table_name}"

job_config = bigquery.LoadJobConfig(
    autodetect=True,
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
)

load_job = client.load_table_from_uri(
    file_location, table_id, job_config=job_config
)

load_job.result()

# read out the newly written table
destination_table = client.get_table(table_id)

print("Loaded {} rows.".format(destination_table.num_rows))

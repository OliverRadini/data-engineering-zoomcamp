from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task()
def extract_from_gcs(color, year, month):
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("de-zoomcamp")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data")
    return Path("../data/{gcs_path}")

@flow()
def etl_gcs_to_bq():
    """Main ETL to load data to biq query"""
    color = "yellow"
    year = 2021
    month = 1

    path = extract_from_gcs(color, year, month)

if __name__ == "__main__":
    etl_gcs_to_bq()
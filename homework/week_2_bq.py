from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract_from_gcs(color, year, month):
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("de-zoomcamp")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data")
    return Path(f"../data/{gcs_path}")

@task()
def to_df(path):
    """read file to dataframe"""
    df = pd.read_parquet(path)
    return df


@task(retries=3)
def write_bq(df):
    """Write dataframe to big query"""
    gcp_credentials_block = GcpCredentials.load("de-zoomcamp-creds")

    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="sturdy-ranger-384021",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )


@flow(log_prints=True)
def etl_gcs_to_bq(color="yellow", year=2021, months=[1]):
    """Main ETL to load data to biq query"""
    for month in months:
        path = extract_from_gcs(color, year, month)
        df = to_df(path)
        print(f">>> For {color} trip data in month {month} in year {year}, there are {len(df)} rows")
        write_bq(df)

if __name__ == "__main__":
    etl_gcs_to_bq()
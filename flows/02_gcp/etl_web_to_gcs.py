from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task()
def write_local(df, color, dataset_file):
    """write dataframe out as a parquet file"""
    directory = Path(f"data/{color}/")
    path = Path(f"{directory}{dataset_file}.parquet")

    directory.mkdir(parents=True, exist_ok=True)

    df.to_parquet(path, compression="gzip")
    return path

@task()
def write_gcs(path):
    """Upload local parquet file to gcs"""
    gcp_cloud_storage_bucket_block = GcsBucket.load("de-zoomcamp")
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=f"{path}", to_path=path)


@task(retries=3)
def fetch(dataset_url):
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def clean(df):
    """Fix some dtype issues"""
    print("=" * 20)
    print("PRE:")
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    print("=" * 20)

    if (hasattr(df, "tpep_pickup_datetime")):
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    else:
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    print("=" * 20)
    print("POST:")
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    print("=" * 20)
    return df


@flow()
def etl_web_to_gcs():
    """The main ETL function"""
    color = "green"
    year = 2020
    month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    local_path = write_local(df_clean, color, dataset_file)
    write_gcs(local_path)

if __name__ == "__main__":
    etl_web_to_gcs()
    
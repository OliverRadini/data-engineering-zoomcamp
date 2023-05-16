import argparse
import pandas as pd
import wget
from prefect_sqlalchemy import SqlAlchemyConnector
from prefect import flow, task
from prefect.tasks import task_input_hash


def get_file_name(url):
    download_file_name = "./{url}".format(url=url.split("/")[-1])
    return download_file_name


def download_from_url(url, output_file_name):
    wget.download(url, out=output_file_name)


def get_dataframe_from_file(download_file_name):
    if ".csv" in download_file_name:
        dataframe = pd.read_csv(download_file_name)
    else:
        dataframe = pd.read_parquet(download_file_name)
    
    return dataframe


def set_dataframe_datetime_attributes(dataframe):
    if (hasattr(dataframe, "tpep_pickup_datetime")):
        dataframe.tpep_pickup_datetime = pd.to_datetime(dataframe.tpep_pickup_datetime)
        dataframe.tpep_dropoff_datetime = pd.to_datetime(dataframe.tpep_dropoff_datetime)
    else:
        dataframe.lpep_pickup_datetime = pd.to_datetime(dataframe.lpep_pickup_datetime)
        dataframe.lpep_dropoff_datetime = pd.to_datetime(dataframe.lpep_dropoff_datetime)


@task(log_prints=True, retries=1)
def run_sql_dataframe(dataframe, table_name, engine):
    dataframe.to_sql(name=table_name, con=engine, if_exists="replace")


@task(log_prints=True, retries=3, cache_key_fn=task_input_hash)
def data_url_to_dataframe(url):
    download_file_name = get_file_name(url)
    download_from_url(url, download_file_name)

    dataframe = get_dataframe_from_file(download_file_name)
    set_dataframe_datetime_attributes(dataframe)
    return dataframe


@flow(name="Ingest flow", retries=0)
def main(url, table_name):
    dataframe = data_url_to_dataframe(url)

    connection_block = SqlAlchemyConnector.load("mainlocalde")
    with connection_block.get_connection(begin=False) as engine:
        run_sql_dataframe(dataframe, table_name, engine)


if (__name__ == "__main__"):
    url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
    table_name="yellow_taxi_data"

    main(url, table_name)

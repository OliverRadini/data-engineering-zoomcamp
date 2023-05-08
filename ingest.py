import argparse
import pandas as pd
import wget
from sqlalchemy import create_engine
from prefect import flow, task


@task(log_prints=True, retries=3)
def get_engine(user, password, host, port, db):
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    return engine


def get_file_name(url):
    download_file_name = "./{url}".format(url=url.split("/")[-1])
    return download_file_name


@task(log_prints=True, retries=5)
def download_from_url(url, output_file_name):
    wget.download(url, out=output_file_name)


@task(log_prints=True, retries=0)
def get_dataframe_from_file(download_file_name):
    if ".csv" in download_file_name:
        dataframe = pd.read_csv(download_file_name)
    else:
        dataframe = pd.read_parquet(download_file_name)
    
    return dataframe


@task(log_prints=True, retries=0)
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


@flow(name="Ingest flow", retries=0)
def main(user, password, host, port, db, url, table_name):
    engine = get_engine(user, password, host, port, db)

    download_file_name = get_file_name(url)
    download_from_url(url, download_file_name)

    dataframe = get_dataframe_from_file(download_file_name)
    set_dataframe_datetime_attributes(dataframe)

    run_sql_dataframe(dataframe, table_name, engine)


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        prog="Parquet taxi data ingestion script",
        description="Ingest data from parquet files and insert them into sql tables"
    )

    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="db for postgres")
    parser.add_argument("--table_name", help="table-name into which data should be inserted")
    parser.add_argument("--url", help="url of the file")

    args = parser.parse_args()

    main(args.user, args.password, args.host, args.port, args.db, args.url, args.table_name)

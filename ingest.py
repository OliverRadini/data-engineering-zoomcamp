import argparse
import pandas as pd
import wget
from sqlalchemy import create_engine

def main(params):
    engine = create_engine(f"postgresql://{params.user}:{params.password}@{params.host}:{params.port}/{params.db}")
    
    parquet_name = "./output.parquet"

    wget.download(params.url, out=parquet_name)

    dataframe = pd.read_parquet(parquet_name)

    if (hasattr(dataframe, "tpep_pickup_datetime")):
        dataframe.tpep_pickup_datetime = pd.to_datetime(dataframe.tpep_pickup_datetime)
        dataframe.tpep_dropoff_datetime = pd.to_datetime(dataframe.tpep_dropoff_datetime)
    else:
        dataframe.lpep_pickup_datetime = pd.to_datetime(dataframe.lpep_pickup_datetime)
        dataframe.lpep_dropoff_datetime = pd.to_datetime(dataframe.lpep_dropoff_datetime)

    dataframe.to_sql(name=params.table_name, con=engine, if_exists="replace")



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

    main(args)
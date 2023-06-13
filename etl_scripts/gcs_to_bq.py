from google.cloud import bigquery

PROJECT_NAME = "sturdy-ranger-384021"
DATASET = "dezoomcamp"
FILE_ROOT = f"gs://dtc_data_lake_sturdy-ranger-384021/data/"


# TODO: make this work with command line arguments

def gcs_to_bq(table_name, file_location):
    client = bigquery.Client()

    table_id = f"{PROJECT_NAME}.{DATASET}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("post_abbr", "STRING"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )

    load_job = client.load_table_from_uri(
        f"{FILE_ROOT}{file_location}", table_id, job_config=job_config
    )

    load_job.result()

    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))
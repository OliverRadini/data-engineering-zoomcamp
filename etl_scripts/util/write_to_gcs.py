from google.cloud import storage

def write_to_gcs(bucket_name, blob_name, contents):
    print(f"Writing to bucket {bucket_name}, blob {blob_name}")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open("w") as f:
        f.write(contents)

    print("Written")

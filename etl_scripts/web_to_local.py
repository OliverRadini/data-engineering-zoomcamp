import pandas as pd
from pathlib import Path

def web_to_local(color, year, month):
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"
    print(f"requesting from {dataset_url}")

    df = pd.read_csv(dataset_url)

    directory = Path(f"data/{color}/")
    path = Path(f"{directory}/{dataset_file}.parquet")

    directory.mkdir(parents=True, exist_ok=True)

    df.to_parquet(path, compression="gzip")


web_to_local("yellow", 2019, 1)
import pandas as pd
from pathlib import Path

from util.parse_standard_args import parse_standard_args

args = parse_standard_args()

def web_to_local(color, year, month):
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"
    print(f"requesting from {dataset_url}")

    df = pd.read_csv(dataset_url)

    directory = Path(f"data/{color}/")
    path = Path(f"{directory}/{dataset_file}.csv")

    directory.mkdir(parents=True, exist_ok=True)

    df.to_csv(path, compression="gzip")

    print(f"""
        Dataframe read 

        {color} for {month}/{year}

        Total rows: {len(df)}
    """)


web_to_local(args.color, args.year, int(args.month))
FROM prefecthq/prefect:2.0.2-python3.10

COPY prefect-requirements.txt .

RUN pip install -r prefect-requirements.txt --trusted-host pypi.python.org --no-cache-dir
RUN mkdir /opt/prefect/flows

COPY flows/02_gcp/parameterised_flow.py /opt/prefect/flows/parameterised_flow.py

# FROM docker.io/python:3

# RUN pip install pandas sqlalchemy psycopg2 wget pyarrow

# WORKDIR /app

# COPY ingest.py ingest.py

# ENTRYPOINT [ "python", "./ingest.py"]


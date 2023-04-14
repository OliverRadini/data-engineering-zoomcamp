FROM docker.io/python:3

RUN pip install pandas sqlalchemy psycopg2 wget pyarrow

WORKDIR /app

COPY ../ingestion_scripts/initial/first.py index.py

CMD [ "python", "./helloworld.py"]
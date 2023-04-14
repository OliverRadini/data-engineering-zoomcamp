FROM docker.io/python:3

RUN pip install pandas sqlalchemy psycopg2 wget pyarrow

WORKDIR /app

COPY ingest.py ingest.py

CMD [ "python", "./helloworld.py"]
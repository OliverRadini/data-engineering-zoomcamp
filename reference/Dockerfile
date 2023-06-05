FROM prefecthq/prefect:2.0.2-python3.10

COPY prefect-requirements.txt .

RUN pip install -r prefect-requirements.txt --trusted-host pypi.python.org --no-cache-dir
RUN mkdir /opt/prefect/flows

COPY flows/03_deployments/parametrised_flow.py /opt/prefect/flows/parameterised_flow.py

# Import libraries
import airflow 
import requests
import json
import pandas as pd
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


# Create Python functions for PythonOperator
def fetch_data():
    url = "https://api.data.gov.sg/v1/transport/carpark-availability"
    response = requests.get(url).json()
    return response


def clean_data(ti):
    # Fetch data from above Airflow Task
    raw = ti.xcom_pull(task_ids = 'fetch_data')                     
    raw = raw['items'][0]['carpark_data']
    raw_df = pd.DataFrame(raw)
 
    # Unnest carpark info which contains multiple values per list
    raw_df = raw_df.explode('carpark_info')

    # Split carpark_info into multiple columns 
    normalize_data = pd.json_normalize(raw_df['carpark_info'])

    # Join back everything and write to csv file 
    raw_df = raw_df.reset_index()
    clean_df = pd.concat([raw_df, normalize_data], axis=1)
    clean_df = clean_df.drop('carpark_info', axis=1)
    clean_df.to_csv('Files.csv')


# Specify DAG default arguments
default_args = {
    'owner': 'bmoh',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}


# Create DAG
with DAG(
    default_args = default_args,
    dag_id = "Carpark_DAG_V1",
    description = 'Webscraping Data pipeline for Carpark API SG',
    start_date = datetime(2022,4,16),
    schedule_interval = "@hourly" 
) as dag:

    # Create workflow operators under the DAG 
    task_1 = PythonOperator(
        task_id = 'fetch_data',
        python_callable = fetch_data
    )

    task_2 = PythonOperator(
       task_id = 'clean_data',
       python_callable= clean_data
    )
    

    # Specify Task order
    task_1 >> task_2

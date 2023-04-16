## Carpark API Airflow
This is a project on using Airflow on Docker to periodically run a certain set of tasks based on Airflow scheduler defined. Specifically, the data pipeline does the following:
1. Scrape data from Carpark API availability website [here](https://api.data.gov.sg/v1/transport/carpark-availability)
2. Take in raw API json data using ```ti.xcom_pull(task_ids = 'XXX') ``` and clean it into a tabular format such as excel file. An example of raw API data looks like this:
    ```
    {'carpark_info': [{'total_lots': '105', 'lot_type': 'C', 'lots_available': '0'}], 'carpark_number': 'HE12', 'update_datetime': '2023-04-15T15:23:01'}
    ```
3. Write the raw API json data to a cleaned csv file

Note that CeleryExecutor is chosen in Airflow which means that parallel tasks are run at the same time and more information can be found at this [website](https://hevodata.com/learn/airflow-parallelism/#2) 


## Configuration Details
Configure [Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/pipeline.html) by following the steps below:
1. Download Docker Desktop and Apache Airflow
2. Download Docker compose yaml file by running:
    - ```curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.3/docker-compose.yaml'```
4. Initialise folder environment by executing:
    - ```mkdir -p ./dags ./logs ./plugins```
    - ```echo -e "AIRFLOW_UID=$(id -u)" > .env```
5. Initialise Airflow Database account by running ```docker compose up airflow-init```
6. Start all Airflow services by running ```docker-compose up -d```
7. Run Airflow webserver by entering ```http://localhost:8080``` with username and password as ```airflow```
8. Check Docker Airflow container status by running ```docker ps```
9. Each time a code edit is made, update the dag_id by appending the version id behind the dag_id (i.e. V1, V2, etc)

## End result
1. Once Airflow is deployed on Docker, you can access webserver link at http://localhost:8080
    - ![plot](Images/Airflow%20login.png)
2. Find the DAG "Carpark_DAG_V1" inside the main UI interface. You can check the task log by clicking onto each individual tasks:
    - ![plot](Images/Airflow%20Main.png)
3. The task ```clean_data``` pulls information from ```fetch_data``` via the function ```ti.xcom_pull(task_ids = 'XXX')```:
    - ![plot](Images/Airflow%20TI%20Xcoms.png)


## Reference
1. [Apache Airflow Docs](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/pipeline.html)
2. [Apache Airflow Youtube Guide](https://www.youtube.com/watch?v=K9AnJ9_ZAXE&t=2594s)
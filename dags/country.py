from datetime import datetime, timedelta
from urllib.request import urlopen
import json
import mysql.connector

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'kartaca',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def welcome_message():
    print("DAG is up and running!")


def get_country_data():
    url = "http://country.io/names.json"
    response = urlopen(url)
    country_json = json.loads(response.read())
    return country_json


def insert_country_data(ti):
    country_json = ti.xcom_pull(task_ids='get_country_data')

    db = mysql.connector.connect(
        user='kartaca',
        password='kartaca',
        host='host.docker.internal',
        database='kartaca',
        port='3307'
    )

    cursor = db.cursor()

    # first deleting the possibly existing data to prevent primary key conflicts
    cursor.execute("DELETE FROM country")

    # inserting the country data
    sql = "INSERT INTO country (country_abbreviation, country_name) VALUES (%s, %s)"
    val = list(country_json.items())
    cursor.executemany(sql, val)
    db.commit()

    cursor.close()
    db.close()


def goodbye_message():
    print("DAG completed its work!")


with DAG(
    dag_id='country',
    default_args=default_args,
    description='This dag fills up the country table',
    start_date=datetime(2023, 3, 18),
    schedule_interval='0 10 * * *'
) as dag:
    task1 = PythonOperator(
        task_id='welcome_message',
        python_callable=welcome_message,
    )

    task2 = PythonOperator(
        task_id='get_country_data',
        python_callable=get_country_data,
    )

    task3 = PythonOperator(
        task_id="insert_country_data",
        python_callable=insert_country_data,
    )

    task4 = PythonOperator(
        task_id='goodbye_message',
        python_callable=goodbye_message,
    )


    task1 >> task2 >> task3 >> task4
from datetime import datetime, timedelta
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


def merge_tables():
    db = mysql.connector.connect(
        user='kartaca',
        password='kartaca',
        host='host.docker.internal',
        database='kartaca',
        port='3307'
    )

    cursor = db.cursor()

    # dropping the table if it exists
    cursor.execute("DROP TABLE IF EXISTS data_merge")

    # creating the data_merge table
    cursor.execute("""
        CREATE TABLE data_merge (
            country_abbreviation VARCHAR(5),
            country_name VARCHAR(100),
            currency VARCHAR(5),
            PRIMARY KEY (country_abbreviation)
        )
    """)

    # merging the country and currency tables and inserting it to the data_merge table
    cursor.execute("""
        INSERT INTO data_merge (country_abbreviation, country_name, currency)
        SELECT country.country_abbreviation, country.country_name, currency.currency
        FROM country
        INNER JOIN currency ON country.country_abbreviation = currency.country_abbreviation
    """)
    db.commit()

    cursor.close()
    db.close()


def goodbye_message():
    print("DAG completed its work!")



with DAG(
    dag_id='data_merge',
    default_args=default_args,
    description='This dag merges country and currency tables',
    start_date=datetime(2023, 3, 18),
    schedule_interval='10 10 * * *'
) as dag:
    task1 = PythonOperator(
        task_id='welcome_message',
        python_callable=welcome_message,
    )

    task2 = PythonOperator(
        task_id='merge_tables',
        python_callable=merge_tables,
    )

    task3 = PythonOperator(
        task_id='goodbye_message',
        python_callable=goodbye_message,
    )


    task1 >> task2 >> task3
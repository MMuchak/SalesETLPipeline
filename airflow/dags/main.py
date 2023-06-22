from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.python.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.postgres_to_s3 import PostgresToS3Operator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
from airflow.utils.email import send_email
import logging

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'email': ['your_email@example.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 6, 22),
}

# Initialize the DAG
dag = DAG(
    'sales_data_pipeline',
    default_args=default_args,
    description='A data pipeline for sales data from PostgreSQL to S3 with data validation',
    schedule_interval=timedelta(days=1),
)

# Define the PostgreSQL incremental extraction task
extract_sql = """
    SELECT * FROM sales WHERE SaleDate > '{{ prev_execution_date }}';
"""
extract_to_s3 = PostgresToS3Operator(
    task_id='extract_to_s3',
    postgres_conn_id='postgres_default',
    sql=extract_sql,
    s3_bucket='your_s3_bucket',
    s3_key='sales_data/{{ ds }}.csv',
    aws_conn_id='aws_default',
    dag=dag,
)

# Define SQL for data validation
check_duplicates_sql = """
    SELECT COUNT(*) = COUNT(DISTINCT id) AS is_unique FROM sales WHERE SaleDate > '{{ prev_execution_date }}';
"""
check_null_values_sql = """
    SELECT COUNT(*) AS null_count FROM sales WHERE Product IS NULL OR Price IS NULL OR SaleDate IS NULL;
"""
check_value_range_sql = """
    SELECT COUNT(*) FROM sales WHERE Price < 0;
"""
check_data_pattern_sql = """
    SELECT COUNT(*) FROM sales WHERE NOT Product ~* '^[A-Za-z0-9 ]+$';
"""

# Define function to evaluate quality check results
def evaluate_quality_checks(**kwargs):
    ti = kwargs['ti']
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    is_unique = postgres_hook.get_first(check_duplicates_sql)[0]
    null_count = postgres_hook.get_first(check_null_values_sql)[0]
    value_range_check = postgres_hook.get_first(check_value_range_sql)[0]
    data_pattern_check = postgres_hook.get_first(check_data_pattern_sql)[0]
    
    error_messages = []
    
    if not is_unique:
        error_messages.append("Duplicate records exist in sales table")
    else:
        logging.info("No duplicate records found in sales table")
    
    if null_count > 0:
        error_messages.append(f"{null_count} null values found in critical columns of sales table")
    else:
        logging.info("No null values found in critical columns of sales table")
    
    if value_range_check > 0:
        error_messages.append(f"{value_range_check} records have negative prices")
    else:
        logging.info("No records with negative prices found")
        
    if data_pattern_check > 0:
        error_messages.append(f"{data_pattern_check} product names do not match the expected pattern")
    else:
        logging.info("All product names matchthe expected pattern")
        
    if error_messages:
        error_text = "Data Quality Checks Failed: " + " | ".join(error_messages)
        logging.error(error_text)
        
        # Send an email notification using Airflow's built-in send_email function
        send_email(
            to=['your_email@example.com'],
            subject='Data Quality Checks Failed',
            html_content=error_text
        )
        raise ValueError(error_text)
    else:
        logging.info("Data Quality Checks Passed Successfully")

# Define the task to evaluate quality checks
evaluate_quality_checks_task = PythonOperator(
    task_id='evaluate_quality_checks',
    python_callable=evaluate_quality_checks,
    provide_context=True,
    dag=dag,
)

# Set up task dependencies
extract_to_s3 >> evaluate_quality_checks_task

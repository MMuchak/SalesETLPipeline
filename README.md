# Sales Data Pipeline

## Overview
This project is an Apache Airflow DAG that automates the extraction, quality checking, and loading of sales data from a PostgreSQL database to Amazon S3. It is also integrated with Snowflake for further data processing and analytics.

## Features
- Incremental extraction of sales data based on the sale date.
- Data quality checks including duplicate detection, null value checking, and data pattern validation.
- Notification on data quality check failure via email.
- Loading of sales data to Amazon S3 in CSV format.
- Snowflake integration for data warehousing.

## Getting Started
To get started with the Sales Data Pipeline, you need to set up the environment, install dependencies, and configure the necessary services. See the [Configuration Guide](docs/configuration_guide.md) for detailed instructions on how to configure and run the Sales Data Pipeline.



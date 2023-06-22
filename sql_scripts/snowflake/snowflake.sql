CREATE TABLE sales (
   Product VARCHAR(20) NOT NULL,
   Price INT NOT NULL,
   SaleDate DATE NOT NULL,
   product_attributes VARIANT
);

CREATE STORAGE INTEGRATION my_s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/MyRole'
  STORAGE_ALLOWED_LOCATIONS = ('s3://mybucket/sales/');

CREATE STAGE my_stage
  URL='s3://mybucket/sales/'
  STORAGE_INTEGRATION = my_s3_integration;

CREATE FILE FORMAT my_file_format
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  NULL_IF = ('');

CREATE TASK my_task
  WAREHOUSE my_warehouse
  SCHEDULE = 'USING CRON 10 0 * * * UTC'
  NOTIFICATION_CHANNEL = 'arn:aws:sns:us-west-2:123456789012:MySNSTopic'
AS
BEGIN
  -- Define variables for error handling
  DECLARE
    v_error_message VARCHAR;
  
  -- Execute the COPY statement to load data from S3 to the table
  COPY INTO sales
  FROM @my_stage
  FILE_FORMAT = (FORMAT_NAME = my_file_format)
  ON_ERROR = 'ABORT_STATEMENT';
  
  -- Check for errors during the COPY operation
  IF (LAST_QUERY_STATUS() <> 'LOADED') THEN
    -- Construct error message
    v_error_message := 'Error loading data from S3 to table: ' || LAST_QUERY_ERROR_MESSAGE();
    
    -- Send error notification via SNS
    SYSTEM$NOTIFY(CHANNEL => 'SNS_CHANNEL', MESSAGE => v_error_message);
  
    -- Log the error message
    SYSTEM$LOG.ERROR(v_error_message);
    
    -- Raise an exception to terminate the task
    RAISE EXCEPTION v_error_message;
  END IF;
END;

import unittest
from unittest.mock import patch, Mock
from airflow.models import DagBag, TaskInstance
from airflow.hooks.postgres_hook import PostgresHook

class TestSalesDataPipeline(unittest.TestCase):
    
    def setUp(self):
        self.dagbag = DagBag()
        self.dag_id = 'sales_data_pipeline'
    
    def test_dag_loaded(self):
        dag = self.dagbag.get_dag(self.dag_id)
        self.assertIsNotNone(dag)
        self.assertEqual(len(dag.tasks), 2)
    
    def test_extract_to_s3_task(self):
        dag = self.dagbag.get_dag(self.dag_id)
        task_id = 'extract_to_s3'
        task = dag.get_task(task_id)
        self.assertIsNotNone(task)
        self.assertEqual(task.task_id, task_id)
        self.assertEqual(task.postgres_conn_id, 'postgres_default')
        self.assertEqual(task.s3_bucket, 'your_s3_bucket')
        self.assertEqual(task.s3_key, 'sales_data/{{ ds }}.csv')
        self.assertEqual(task.aws_conn_id, 'aws_default')
    
    def test_evaluate_quality_checks_task(self):
        dag = self.dagbag.get_dag(self.dag_id)
        task_id = 'evaluate_quality_checks'
        task = dag.get_task(task_id)
        self.assertIsNotNone(task)
        self.assertEqual(task.task_id, task_id)
        self.assertTrue(task.python_callable is not None)
    
    @patch.object(PostgresHook, 'get_first')
    @patch('airflow.utils.email.send_email')
    def test_quality_check_sql_queries(self, mock_send_email, mock_get_first):
        dag = self.dagbag.get_dag(self.dag_id)
        task_id = 'evaluate_quality_checks'
        task = dag.get_task(task_id)
        
        # Mock the PostgresHook and the SQL query results
        mock_get_first.side_effect = [(True,), (0,), (0,), (0,)]
        
        # Mock the TaskInstance
        mock_ti = Mock(spec=TaskInstance)
        
        # Call the python_callable
        task.python_callable(ti=mock_ti)
        
        # Assert send_email was not called
        mock_send_email.assert_not_called()

    def test_task_dependencies(self):
        dag = self.dagbag.get_dag(self.dag_id)
        extract_to_s3_task = dag.get_task('extract_to_s3')
        evaluate_quality_checks_task= dag.get_task('evaluate_quality_checks')
        self.assertTrue(evaluate_quality_checks_task in extract_to_s3_task.downstream_list, "Task dependencies not set correctly")

    def tearDown(self):
        self.dagbag = None

if __name__ == '__main__':
    unittest.main()

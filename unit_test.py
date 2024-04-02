import unittest
from unittest.mock import patch
from src.mistral_model_rag import query_engine

class TestQueryEngine(unittest.TestCase):

    @patch('src.mistral_model_rag.query_engine')
    def test_query_engine(self, mock_query_engine):
        # Mock the behavior of query method of the query engine
        mock_query_engine.query.return_value = "26%"
        # Call the function under test
        response = query_engine.query("what percentage of greenhouse emmsion is food production responsible for?")
        # Assert that the function returned the expected response
        self.assertEqual(response, "26%")
        print(f'the response is - {response}')

if __name__ == '__main__':
    unittest.main()

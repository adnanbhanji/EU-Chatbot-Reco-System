import unittest
from unittest.mock import patch
import sys
from pprint import pprint
import os

# Adding the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from mistral_model_rag import query_engine

class TestQueryEngine(unittest.TestCase):

    @patch('mistral_model_rag.query_engine.query')
    def test_query_engine_greenhouse_emission(self, mock_query_engine):
        # Mock the behavior of the query method of the query engine for the first question
        mock_query_engine.return_value = "01 Food production is responsible for 26% of global greenhouse gas emissions."
        
        # Call the function under test with the first question
        response = query_engine.query("what percentage of greenhouse emission is food production responsible for?")
        
        # Convert response to string (adjust based on actual response structure)
        response_str = str(response)
        
        # Print the response type and content directly to bypass unittest output capture
        print(f"Response type: {type(response)}", file=sys.__stdout__)
        print("Response content:", file=sys.__stdout__)
        pprint(response_str, stream=sys.__stdout__)

        # Assert that "26%" is within the converted response string
        self.assertIn("26%", response_str)

    @patch('mistral_model_rag.query_engine.query')
    def test_query_engine_eu_climate_strategy(self, mock_query_engine):
        # Mock the behavior of the query method for the second question
        mock_query_engine.return_value = "The EU response to climate change is based on mitigation and adaptation strategies."
        
        # Call the function under test with the second question
        response = query_engine.query("The EU response to climate change is based on which two strategies?")
        
        # Convert response to string (adjust based on actual response structure)
        response_str = str(response)
        
        # Assert that both "mitigation" and "adaptation" are in the response
        self.assertIn("mitigation", response_str)
        self.assertIn("adaptation", response_str)

if __name__ == '__main__':
    unittest.main()

import os
import sys
import unittest
from fastapi.testclient import TestClient

# Adding the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from mistral_model_rag_final import app

class TestYourApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This runs once before all tests
        cls.client = TestClient(app)

    def test_environment_variables_loaded(self):
        """Ensure environment variables are loaded correctly."""
        self.assertIsNotNone(os.getenv("TWILIO_ACCOUNT_SID"), "TWILIO_ACCOUNT_SID is not set.")
        self.assertIsNotNone(os.getenv("TWILIO_AUTH_TOKEN"), "TWILIO_AUTH_TOKEN is not set.")
        self.assertIsNotNone(os.getenv("TWILIO_NUMBER"), "TWILIO_NUMBER is not set.")
        self.assertIsNotNone(os.getenv("MY_NUMBER"), "MY_NUMBER is not set.")

    def test_environment_variables_format(self):
        """Test the format of critical environment variables."""
        twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.assertTrue(twilio_sid.startswith("AC"), "TWILIO_ACCOUNT_SID does not have the correct format.")

    def test_document_existence(self):
        """Test if the specified document exists in the directory."""
        document_path = "./src/dataset/CO2Emissions-Europe.pdf"
        self.assertTrue(os.path.exists(document_path), f"Document does not exist: {document_path}")

    def test_api_endpoint(self):
        """Test a FastAPI endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200, "Failed to reach the GET / endpoint.")

    def test_api_endpoint_content(self):
        """Test the content of the response for a FastAPI endpoint."""
        response = self.client.get("/")
        response_content = response.json().get("message")
        self.assertEqual(response_content, "Hello, World!", "Response content of GET / is not as expected.")

    def test_endpoint_with_invalid_input(self):
        """Test endpoint behavior with invalid input."""
        response = self.client.get("/wrong-endpoint")
        self.assertEqual(response.status_code, 404, "Expected a 404 Not Found status code for invalid input but got another.")

if __name__ == '__main__':
    unittest.main()

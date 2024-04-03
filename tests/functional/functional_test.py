import unittest
import os
from fastapi.testclient import TestClient
import sys
from github import secrets  # Import the 'secrets' module

# Adding the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), '..', '..', 'src')))
from mistral_model_rag import app  # Adjust the import according to your application structure

class TestYourApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This runs once before all tests
        cls.client = TestClient(app)

        # Retrieve Twilio credentials from GitHub secrets
        cls.twilio_account_sid = secrets.TWILIO_ACCOUNT_SID
        cls.twilio_auth_token = secrets.TWILIO_AUTH_TOKEN
        cls.twilio_number = secrets.TWILIO_NUMBER
        cls.my_number = secrets.MY_NUMBER

    def test_environment_variables_loaded(self):
        """Ensure environment variables are loaded correctly."""
        self.assertIsNotNone(self.twilio_account_sid)
        self.assertIsNotNone(self.twilio_auth_token)
        self.assertIsNotNone(self.twilio_number)
        self.assertIsNotNone(self.my_number)

    def test_environment_variables_format(self):
        """Test the format of critical environment variables."""
        twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.assertTrue(twilio_sid.startswith("AC"), "TWILIO_ACCOUNT_SID does not have the correct format.")

    def test_document_existence(self):
        """Test if the specified document exists in the directory."""
        document_path = "./src/new/CO2Emissions-Europe.pdf"
        self.assertTrue(os.path.exists(document_path), f"Document does not exist: {document_path}")

    def test_api_endpoint(self):
        """Test a FastAPI endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_api_endpoint_content(self):
        """Test the content of the response for a FastAPI endpoint."""
        response = self.client.get("/")
        response_content = response.json().get("message")
        self.assertEqual(response_content, "Hello, World!", "Response content is not as expected.")

    def test_endpoint_with_invalid_input(self):
        """Test endpoint behavior with invalid input."""
        response = self.client.get("/wrong-endpoint")
        self.assertEqual(response.status_code, 404, "Expected a 404 Bad Request status code for invalid input.")

if __name__ == '__main__':
    unittest.main()

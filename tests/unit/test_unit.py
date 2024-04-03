import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Adding the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'llama2_whatsapp_bot')))
from llamapp import app, WhatsAppClient

class TestWhatsAppClient(unittest.TestCase):
    @patch('requests.post')
    def test_send_text_message_success(self, mock_post):
        mock_post.return_value.status_code = 200
        client = WhatsAppClient()
        status = client.send_text_message("Test message", "123456789")
        self.assertEqual(status, 200)

    @patch('requests.post')
    def test_send_text_message_failure(self, mock_post):
        mock_post.return_value.status_code = 500
        client = WhatsAppClient()
        status = client.send_text_message("Test message", "123456789")
        self.assertNotEqual(status, 200)

class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_root_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello Llama 2", response.data)

    # Add more tests here to simulate POST requests and other scenarios

if __name__ == '__main__':
    unittest.main()

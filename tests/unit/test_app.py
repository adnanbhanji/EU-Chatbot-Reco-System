import unittest
from flask import json
import sys
import os

# Adding the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_whatsapp_status_get(self):
        # Test GET request
        response = self.app.get('/wastatus')
        self.assertEqual(response.status_code, 204)

    def test_whatsapp_status_post_json(self):
        # Test POST request with JSON data
        json_data = {"key": "value"}
        response = self.app.post('/wastatus', json=json_data)
        self.assertEqual(response.status_code, 204)

    def test_whatsapp_status_post_form(self):
        # Test POST request with form data
        form_data = {"key": "value"}
        response = self.app.post('/wastatus', data=form_data)
        self.assertEqual(response.status_code, 204)

    def test_receive_message(self):
        # Test POST request with JSON data
        json_data = {
            "message_type": "text",
            "to": "recipient",
            "from": "sender",
            "channel": "whatsapp",
            "text": "Hello"
        }
        response = self.app.post('/', json=json_data)
        self.assertEqual(response.status_code, 200)

unittest.main()

import unittest
import requests
import json
import unittest
from flask import json
import sys
import os

# Adding the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from app import app

class TestAppIntegration(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_whatsapp_status_get(self):
        response = self.app.get('/wastatus')
        self.assertEqual(response.status_code, 204)

    def test_whatsapp_status_post_json(self):
        json_data = {
            "message_type": "text",
            "to": "recipient",
            "from": "sender",
            "channel": "whatsapp",
            "text": "Hello"
        }
        response = self.app.post('/wastatus', json=json_data)
        self.assertEqual(response.status_code, 204)

    def test_whatsapp_status_post_form(self):
        form_data = {
            "message_type": "text",
            "to": "recipient",
            "from": "sender",
            "channel": "whatsapp",
            "text": "Hello"
        }
        response = self.app.post('/wastatus', data=form_data)
        self.assertEqual(response.status_code, 204)

    def test_receive_message(self):
        json_data = {
            "message_type": "text",
            "to": "recipient",
            "from": "sender",
            "channel": "whatsapp",
            "text": "Hello"
        }
        response = self.app.post('/', json=json_data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

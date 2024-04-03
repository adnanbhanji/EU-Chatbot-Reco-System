import unittest
import requests_mock
import os
import sys

# Adding the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'llama2_whatsapp_bot')))
from llamapp import app, user_responses, user_interactions

class TestMessageReception(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_message_reception_and_response(self):
        # Simulate sending a "start report" message
        response = self.client.get('/msgrcvd', query_string={'message': 'start report'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('What\'s the name of your farm?', response.get_data(as_text=True))

        # Follow-up with answering the first question
        response = self.client.get('/msgrcvd', query_string={'message': 'Sunny Farm'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('What is your name?', response.get_data(as_text=True))

class TestStateTransition(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.destination_number = "34654431185"  # Example destination number

    def test_state_transition_and_data_persistence(self):
        # Start the report and answer the first question
        self.client.get('/msgrcvd', query_string={'message': 'start report', 'number': self.destination_number})
        self.client.get('/msgrcvd', query_string={'message': 'Sunny Farm', 'number': self.destination_number})
        
        # Verify that the response has been saved
        self.assertIn(self.destination_number, user_responses)
        self.assertIn('farm_name', user_responses[self.destination_number])
        self.assertEqual(user_responses[self.destination_number]['farm_name'], 'Sunny Farm')

class TestSpecialCommands(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.destination_number = "34654431185"

    def test_handling_solved_command(self):
        # Simulate an interruption with a question
        self.client.get('/msgrcvd', query_string={'message': 'How does this work?', 'number': self.destination_number})
        self.assertEqual(user_interactions[self.destination_number], 'question')
        
        # Simulate receiving "solved" to clear the interruption
        self.client.get('/msgrcvd', query_string={'message': 'solved', 'number': self.destination_number})
        self.assertNotIn(self.destination_number, user_interactions)

if __name__ == '__main__':
    unittest.main()
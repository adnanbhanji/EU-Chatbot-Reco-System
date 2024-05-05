import unittest
from unittest.mock import patch, MagicMock
from src.commands import is_valid_name, is_valid_number, process_message, handle_response, create_report_content, user_states, user_info
import sys
import os

# Adding the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from app import app

class TestChatbot(unittest.TestCase):

    def test_is_valid_name_with_valid_name(self):
        self.assertTrue(is_valid_name("Farm Sunset"))

    def test_is_valid_name_with_numbers(self):
        self.assertFalse(is_valid_name("Farm123"))

    def test_is_valid_name_with_special_characters(self):
        self.assertFalse(is_valid_name("Farm*"))

    def test_is_valid_name_with_empty_string(self):
        self.assertFalse(is_valid_name(""))

    def test_is_valid_number_with_integer(self):
        self.assertTrue(is_valid_number("100"))

    def test_is_valid_number_with_float(self):
        self.assertTrue(is_valid_number("100.5"))

    def test_is_valid_number_with_negative(self):
        self.assertTrue(is_valid_number("-50"))

    def test_is_valid_number_with_non_numeric(self):
        self.assertFalse(is_valid_number("fifty"))

    @patch('your_chatbot_module.send_whatsapp_msg')
    def test_process_message_with_question(self, mock_send):
        req_data = {'from': '12345', 'text': 'How large is your farm?'}
        process_message(req_data)
        mock_send.assert_called_once()

    @patch('your_chatbot_module.send_whatsapp_msg')
    def test_process_message_with_command_start_report(self, mock_send):
        req_data = {'from': '12345', 'text': 'start report'}
        process_message(req_data)
        self.assertEqual(user_states['12345'], 'farm_name')

    @patch('your_chatbot_module.send_whatsapp_msg')
    def test_process_message_with_answer(self, mock_send):
        user_states['12345'] = 'farm_name'
        req_data = {'from': '12345', 'text': 'Sunshine Acres'}
        process_message(req_data)
        self.assertEqual(user_info['12345']['farm_name'], 'Sunshine Acres')

    @patch('your_chatbot_module.send_whatsapp_msg')
    def test_handle_response_for_valid_name(self, mock_send):
        user_states['12345'] = 'farm_name'
        handle_response('12345', 'Green Valley')
        self.assertEqual(user_info['12345']['farm_name'], 'Green Valley')

    @patch('your_chatbot_module.send_whatsapp_msg')
    def test_handle_response_for_invalid_name(self, mock_send):
        user_states['12345'] = 'farm_name'
        handle_response('12345', '1234Green')
        mock_send.assert_called_with('12345', "Please enter a valid name for your farm.")

    @patch('your_chatbot_module.send_whatsapp_msg')
    def test_handle_response_moves_to_next_question(self, mock_send):
        user_states['12345'] = 'farm_name'
        handle_response('12345', 'Green Valley')
        self.assertEqual(user_states['12345'], 'location')  # Assuming 'location' is next in the question order

    def test_create_report_content_formats_correctly(self):
        user_responses = {
            'farm_name': 'Sunset Farm',
            'location': '123 Farm Road, Farmville, Earth',
            'farm_area': '150'
        }
        content = create_report_content(user_responses)
        expected_content = "Farm Report\n\nFarm name: Sunset Farm\nLocation: 123 Farm Road, Farmville, Earth\nFarm area: 150\n"
        self.assertEqual(content, expected_content)

    @patch('your_chatbot_module.send_whatsapp_msg')
    def test_process_message_with_unexpected_input(self, mock_send):
        req_data = {'from': '12345', 'text': 'Unexpected input here'}
        process_message(req_data)
        mock_send.assert_called_with('12345', "Please start the report by typing 'start report'.")

    @patch('your_chatbot_module.send_whatsapp_msg')
    def test_process_message_no_state_initiated(self, mock_send):
        req_data = {'from': '12345', 'text': 'report'}
        process_message(req_data)
        mock_send.assert_called_with('12345', "Please start the report by typing 'start report'.")

if __name__ == '__main__':
    unittest.main()

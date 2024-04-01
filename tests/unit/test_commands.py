import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Adding the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from commands import *

class TestCommands(unittest.TestCase):

    def test_help(self):
        req_data = {}
        response = help(req_data)
        self.assertEqual(response, "Ask me anything...")

    def test_is_valid_name(self):
        self.assertTrue(is_valid_name("John Doe"))
        self.assertFalse(is_valid_name("123"))

    def test_is_valid_number(self):
        self.assertTrue(is_valid_number("123.45"))
        self.assertFalse(is_valid_number("abc"))

 

if __name__ == '__main__':
    unittest.main()
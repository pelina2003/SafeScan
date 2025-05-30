import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forum_controller import ForumController
from user import User

# Mock DBManager προσωρινά
import db_manager
class MockDBManager:
    @staticmethod
    def save_message(forum_id, username, content):
        return True

class TestSubmitMessage(unittest.TestCase):

    def setUp(self):
        self.controller = ForumController()
        db_manager.DBManager.save_message = MockDBManager.save_message

    def test_empty_message(self):
        user = User(username="maria")
        result = self.controller.submit_message(forum_id=1, user=user, content="   ")
        self.assertFalse(result)

    def test_valid_message(self):
        user = User(username="kostas")
        result = self.controller.submit_message(forum_id=1, user=user, content="Καλησπέρα σε όλους!")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()

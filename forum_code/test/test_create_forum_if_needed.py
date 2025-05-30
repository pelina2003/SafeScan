import unittest
from forum_controller import ForumController
from report import Report

class TestCreateForumIfNeeded(unittest.TestCase):

    def setUp(self):
        self.controller = ForumController()

    def test_create_new_forum(self):
        report = Report(risk_type="fire", lat=38.1, lon=23.7)
        # υποθέτουμε ότι δεν υπάρχει παρόμοιο forum
        DBManager.find_similar_forum = lambda *args: None
        DBManager.create_forum = lambda r: print("Forum created")
        result = self.controller.create_forum_if_needed(report)
        self.assertTrue(result)

    def test_forum_already_exists(self):
        report = Report(risk_type="fire", lat=38.1, lon=23.7)
        DBManager.find_similar_forum = lambda *args: object()
        result = self.controller.create_forum_if_needed(report)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

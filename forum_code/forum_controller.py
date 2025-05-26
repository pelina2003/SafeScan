from forum import Forum
from message import Message
from db_manager import DBManager  # (ή database.py)

class ForumController:
    def __init__(self):
        pass

    def create_forum_if_needed(self, report):
        existing = DBManager.find_similar_forum(report.type, report.latitude, report.longitude)
        if existing:
            return existing  # Εναλλακτική ροή 1
        return DBManager.create_forum(report)

    def get_all_forums(self):
        forums = DBManager.get_all_forums()
        if not forums:
            return []  # Εναλλακτική ροή 3
        return forums

    def get_messages_for_forum(self, forum_id):
        return DBManager.get_forum_messages(forum_id)

    def submit_message(self, forum_id, user, content):
        success = DBManager.save_message(forum_id, user.username, content)
        return success  # Εναλλακτική ροή 4 αν false

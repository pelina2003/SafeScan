class Message:
    def __init__(self, message_id, content, author, timestamp, forum_id):
        self.id = message_id
        self.content = content
        self.author = author  # τύπου User
        self.timestamp = timestamp
        self.forum_id = forum_id

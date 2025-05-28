class Forum:
    def __init__(self, forum_id, topic, risk_type, location, created_at):
        self.id = forum_id
        self.topic = topic
        self.risk_type = risk_type
        self.location = location
        self.created_at = created_at
        self.messages = []  # optional

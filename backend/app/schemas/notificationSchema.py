from datetime import datetime

from bson import ObjectId


class Notification:
    """
    A schema for notifications stored in MongoDB.
    """

    def __init__(self, user_id: ObjectId, type: str, content: str, metadata: dict = None):
        self.user_id = user_id
        self.type = type  # e.g., "email", "SMS", "push"
        self.content = content  # Message content
        self.is_read = False  # Default unread
        self.metadata = metadata or {}  # Additional data (e.g., links, actions)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

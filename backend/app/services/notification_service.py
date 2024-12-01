from datetime import datetime

from bson import ObjectId


class NotificationService:
    """
    Service layer for managing notifications stored in MongoDB.
    """

    def __init__(self, db):
        """
        Initialize the NotificationService with a MongoDB database connection.

        Args:
            db: MongoDB database connection.
        """
        self.db = db
        self.collection = self.db["notifications"]  # MongoDB collection name

    async def create_notification(self, user_id: ObjectId, type: str, content: str, metadata: dict | None = None) -> str:
        """
        Create a new notification.

        Args:
            user_id (ObjectId): The user receiving the notification.
            type (str): Type of notification (e.g., email, push).
            content (str): Notification message.
            metadata (Optional[dict]): Additional information or actions.

        Returns:
            str: The ID of the created notification.
        """
        notification = {
            "user_id": user_id,
            "type": type,
            "content": content,
            "is_read": False,
            "metadata": metadata or {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await self.collection.insert_one(notification)
        return str(result.inserted_id)

    async def get_notifications_for_user(self, user_id: ObjectId, limit: int = 100) -> list[dict]:
        """
        Retrieve all notifications for a specific user.

        Args:
            user_id (ObjectId): The user whose notifications to fetch.
            limit (int): Maximum number of notifications to return (default: 100).

        Returns:
            List[dict]: List of notifications for the user.
        """
        notifications = await self.collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit).to_list(length=limit)
        return notifications

    async def mark_notification_as_read(self, notification_id: str) -> bool:
        """
        Mark a notification as read.

        Args:
            notification_id (str): The ID of the notification to mark as read.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        result = await self.collection.update_one(
            {"_id": ObjectId(notification_id)},
            {"$set": {"is_read": True, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0

    async def delete_notification(self, notification_id: str) -> bool:
        """
        Delete a notification by its ID.

        Args:
            notification_id (str): The ID of the notification to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        result = await self.collection.delete_one({"_id": ObjectId(notification_id)})
        return result.deleted_count > 0

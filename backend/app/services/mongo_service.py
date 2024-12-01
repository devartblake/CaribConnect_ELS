from bson import ObjectId


async def create_item(mongo_db, collection: str, data: dict) -> str:
    """
    Create a new document in a specified collection.

    Args:
        mongo_db: The MongoDB database instance.
        collection (str): The collection name.
        data (dict): The data to insert.

    Returns:
        str: The ID of the inserted document.
    """
    result = await mongo_db[collection].insert_one(data)
    return str(result.inserted_id)

async def get_item(mongo_db, collection: str, item_id: str) -> dict | None:
    """
    Retrieve a document by ID from a collection.

    Args:
        mongo_db: The MongoDB database instance.
        collection (str): The collection name.
        item_id (str): The ID of the document to retrieve.

    Returns:
        dict | None: The document if found, else None.
    """
    item = await mongo_db[collection].find_one({"_id": ObjectId(item_id)})
    return item

async def update_item(mongo_db, collection: str, item_id: str, data: dict) -> bool:
    """
    Update a document in a collection.

    Args:
        mongo_db: The MongoDB database instance.
        collection (str): The collection name.
        item_id (str): The ID of the document to update.
        data (dict): The fields to update.

    Returns:
        bool: True if a document was updated, otherwise False.
    """
    result = await mongo_db[collection].update_one(
        {"_id": ObjectId(item_id)}, {"$set": data}
    )
    return result.modified_count > 0

async def delete_item(mongo_db, collection: str, item_id: str) -> bool:
    """
    Delete a document by ID from a collection.

    Args:
        mongo_db: The MongoDB database instance.
        collection (str): The collection name.
        item_id (str): The ID of the document to delete.

    Returns:
        bool: True if a document was deleted, otherwise False.
    """
    result = await mongo_db[collection].delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count > 0

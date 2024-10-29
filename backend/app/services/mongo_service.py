from app.core.db import mongodb
from bson import ObjectId

async def create_item(collection: str, data: dict):
    result = await mongodb.db[collection].insert_one(data)
    return str(result.inserted_id)

async def get_item(collection: str, item_id: str):
    item = await mongodb.db[collection].find_one({"_id": ObjectId(item_id)})
    return item

async def update_item(collection: str, item_id: str, data: dict):
    await mongodb.db[collection].update_one({"_id": ObjectId(item_id)}, {"$set": data})

async def delete_item(collection: str, item_id: str):
    await mongodb.db[collection].delete_one({"_id": ObjectId(item_id)})

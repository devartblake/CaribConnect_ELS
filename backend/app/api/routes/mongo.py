from fastapi import APIRouter, Depends
from app.models import User
from sqlmodel import Session, select
from app.core.db import get_database_session, get_mongodb

router = APIRouter()

@router.get("/sql-data")
async def get_sql_data(db: Session = Depends(get_database_session)):
    # SQLModel query example
    users = db.exec(select(User)).all()
    return users

@router.get("/mongo-data")
async def get_mongo_data(mongodb=Depends(get_mongodb)):
    # MongoDB query example
    items = await mongodb["your_collection"].find().to_list(100)
    return items
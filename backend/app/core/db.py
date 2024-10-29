from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate
from motor.motor_asyncio import AsyncIOMotorClient

# Create the SQLAlchemy (SQLModel)
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
SessionLocal = Session(autocommit=False, autoflush=False, bind=engine)

# Initialize MongoDB (Motor) setup
mongodb_client: AsyncIOMotorClient = None
mongodb_db = None

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28

# Initialize the database with a superuser if not present
def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine) # Create tables (prefer using migrations with Alembic)

    # Check if the superuser already exists
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:

        # Create superuser if not found
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

# Dependency to get a session
def get_database_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize MongoDB
async def init_mongo():
    global mongodb_client, mongodb_db
    mongodb_client = AsyncIOMotorClient(settings.MONGO_URI)
    mongodb_db = mongodb_client[settings.MONGO_DB_NAME]

async def close_mongo_connection():
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        
# Dependency to get MongoDB connection
def get_mongodb():
    return mongodb_db
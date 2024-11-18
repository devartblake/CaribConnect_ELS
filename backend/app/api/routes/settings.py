import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session
from app.models import Settings, Status
from app.schemas.settingsSchema import SettingsCreateSchema, SettingsUpdateSchema, StatusCreateSchema, StatusUpdateSchema
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=Settings)
async def create_settings(settings: SettingsCreateSchema, db: Session = Depends(get_db)):
    db_settings = Settings(**settings.dict())
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings

@router.get("/{settings_id}", response_model=Settings)
async def get_settings(settings_id: uuid.UUID, db: Session = Depends(get_db)):
    db_settings = db.query(Settings).filter(Settings.id == settings_id).first()
    if db_settings is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found")
    return db_settings

@router.put("/{settings_id}", response_model=Settings)
async def update_settings(settings_id: uuid.UUID, settings: SettingsUpdateSchema, db: Session = Depends(get_db)):
    db_settings = db.query(Settings).filter(Settings.id == settings_id).first()
    if db_settings is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found")
    for key, value in settings.dict(exclude_unset=True).items():
        setattr(db_settings, key, value)
    db.commit()
    db.refresh(db_settings)
    return db_settings

@router.delete("/{settings_id}")
async def delete_settings(settings_id: uuid.UUID, db: Session = Depends(get_db)):
    db_settings = db.query(Settings).filter(Settings.id == settings_id).first()
    if db_settings is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found")
    db.delete(db_settings)
    db.commit()
    return {"detail": "Settings deleted"}

# Status
@router.post("/status/", response_model=Status)
async def create_status(status: StatusCreateSchema, db: Session = Depends(get_db)):
    db_status = Status(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

@router.get("/status/{status_id}", response_model=Status)
async def get_status(status_id: uuid.UUID, db: Session = Depends(get_db)):
    db_status = db.query(Status).filter(Status.id == status_id).first()
    if db_status is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status not found")
    return db_status

@router.put("/status/{status_id}", response_model=Status)
async def update_status(status_id: uuid.UUID, status: StatusUpdateSchema, db: Session = Depends(get_db)):
    db_status = db.query(Status).filter(Status.id == status_id).first()
    if db_status is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status not found")
    for key, value in status.dict(exclude_unset=True).items():
        setattr(db_status, key, value)
    db.commit()
    db.refresh(db_status)
    return db_status

@router.delete("/status/{status_id}")
async def delete_status(status_id: uuid.UUID, db: Session = Depends(get_db)):
    db_status = db.query(Status).filter(Status.id == status_id).first()
    if db_status is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status not found")
    db.delete(db_status)
    db.commit()
    return {"detail": "Status deleted"}
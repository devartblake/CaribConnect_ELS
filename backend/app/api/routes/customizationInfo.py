import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.models import CustomizationInfo
from app.schemas.customizationInfoSchema import CustomizationInfoCreate, CustomizationInfoUpdate
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=CustomizationInfo)
async def create_customization_info(customization_info: CustomizationInfoCreate, db: Session = Depends(get_db)):
    db_customization_info = CustomizationInfo(**customization_info.dict())
    db.add(db_customization_info)
    db.commit()
    db.refresh(db_customization_info)
    return db_customization_info

@router.get("/{customizationinfo_id}", response_model=CustomizationInfo)
async def get_customization_info(customization_info_id: uuid.UUID, db: Session = Depends(get_db)):
    db_customization_info = db.query(CustomizationInfo).filter(CustomizationInfo.id == customization_info_id).first()
    if db_customization_info is None:
        raise HTTPException(status_code=404, detail="CustomizationInfo not found")
    return db_customization_info

@router.put("/{customizationinfo_id}", response_model=CustomizationInfo)
async def update_customization_info(customization_info_id: uuid.UUID, customization_info: CustomizationInfoUpdate, db: Session = Depends(get_db)):
    db_customization_info = db.query(CustomizationInfo).filter(CustomizationInfo.id == customization_info_id).first()
    if db_customization_info is None:
        raise HTTPException(status_code=404, detail="CustomizationInfo not found")
    for key, value in customization_info.dict(exclude_unset=True).items():
        setattr(db_customization_info, key, value)
    db.commit()
    db.refresh(db_customization_info)
    return db_customization_info

@router.delete("/{customizationinfo_id}")
async def delete_customization_info(customization_info_id: uuid.UUID, db: Session = Depends(get_db)):
    db_customization_info = db.query(CustomizationInfo).filter(CustomizationInfo.id == customization_info_id).first()
    if db_customization_info is None:
        raise HTTPException(status_code=404, detail="CustomizationInfo not found")
    db.delete(db_customization_info)
    db.commit()
    return {"detail": "CustomizationInfo deleted"}

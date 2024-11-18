from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session
from app.models import AuditInfo
from app.schemas.auditInfoSchema import AuditInfoCreate, AuditInfoRead
from app.api.deps import get_db
from typing import List
import uuid

router = APIRouter()

# Get AuditInfo by ID
@router.get("/{id}", response_model=AuditInfoRead)
async def get_audit_info(id: uuid.UUID, session: Session = Depends(get_db)):
    audit_info = session.get(AuditInfo, id)
    if not audit_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditInfo not found")
    return audit_info

# Create new AuditInfo
@router.post("/", response_model=AuditInfoRead)
async def create_audit_info(audit_info: AuditInfoCreate, session: Session = Depends(get_db)):
    session.add(audit_info)
    session.commit()
    session.refresh(audit_info)
    return audit_info

# Update AuditInfo by ID
@router.put("/{id}", response_model=AuditInfoRead)
async def update_audit_info(id: uuid.UUID, audit_info: AuditInfoCreate, session: Session = Depends(get_db)):
    existing_audit_info = session.get(AuditInfo, id)
    if not existing_audit_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditInfo not found")
    for field, value in audit_info.dict(exclude_unset=True).items():
        setattr(existing_audit_info, field, value)
    session.add(existing_audit_info)
    session.commit()
    session.refresh(existing_audit_info)
    return existing_audit_info

# Delete AuditInfo by ID
@router.delete("/{id}", response_model=AuditInfoRead)
async def delete_audit_info(id: uuid.UUID, session: Session = Depends(get_db)):
    audit_info = session.get(AuditInfo, id)
    if not audit_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditInfo not found")
    session.delete(audit_info)
    session.commit()
    return audit_info

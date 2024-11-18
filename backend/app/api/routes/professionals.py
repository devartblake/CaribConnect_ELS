import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from app.api.deps import get_db
from app.models import Professional
from app.schemas.professionalSchema import ProfessionalCreateSchema, ProfessionalUpdateSchema, ProfessionalResponseSchema

router = APIRouter()

# PROFESSIONAL ROUTES

@router.post("/", response_model=ProfessionalResponseSchema, status_code=status.HTTP_201_CREATED)
def create_professional(professional: ProfessionalCreateSchema, session: Session = Depends(get_db)):
    new_professional = Professional.from_orm(professional)
    session.add(new_professional)
    session.commit()
    session.refresh(new_professional)
    return new_professional

@router.put("/{professional_id}", response_model=ProfessionalResponseSchema, status_code=status.HTTP_200_OK)
def update_professional(professional_id: uuid.UUID, updates: ProfessionalUpdateSchema, session: Session = Depends(get_db)):
    professional = session.get(Professional, professional_id)
    if not professional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professional not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(professional, key, value)
    session.add(professional)
    session.commit()
    session.refresh(professional)
    return professional

@router.delete("/{professional_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professional(professional_id: uuid.UUID, session: Session = Depends(get_db)):
    professional = session.get(Professional, professional_id)
    if not professional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professional not found")
    session.delete(professional)
    session.commit()
    return {"message": "Professional deleted successfully"}

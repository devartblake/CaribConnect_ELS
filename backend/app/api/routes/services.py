import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models import Service
from app.schemas.serviceSchema import ServiceCreate, ServiceUpdate, ServiceRead
from app.api.deps import get_db

router = APIRouter()


# Get all services
@router.get("/", response_model=list[Service])
async def get_all_services(session: Session = Depends(get_db)):
    services = session.query(Service).all()
    return services

# Get service by ID
@router.get("/{service_id}", response_model=Service)
async def get_service(service_id: uuid.UUID, session: Session = Depends(get_db)):
    service = session.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service

# Create a new service
@router.post("/", response_model=ServiceRead)
async def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

# Update service by ID
@router.put("/{service_id}", response_model=Service)
async def update_service(service_id: uuid.UUID, service: ServiceUpdate, session: Session = Depends(get_db)):
    existing_service = session.get(Service, service_id)
    if not existing_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    for key, value in service.dict(exclude_unset=True).items():
        setattr(existing_service, key, value)
    session.add(existing_service)
    session.commit()
    session.refresh(existing_service)
    return existing_service

# Delete service by ID
@router.delete("/{service_id}")
async def delete_service(service_id: uuid.UUID, session: Session = Depends(get_db)):
    service = session.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    session.delete(service)
    session.commit()
    return {"detail": "Service deleted"}

@router.get("/", response_model=list[ServiceRead])
def list_services(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Service).offset(skip).limit(limit).all()
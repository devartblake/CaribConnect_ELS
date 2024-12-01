
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_db  # Assuming you have a dependency to manage sessions
from app.core.db import engine
from app.models import GeoLocation, IPAddress
from app.schemas.ipvSchema import (
    GeoLocationCreateSchema,
    GeoLocationReadSchema,
    GeoLocationUpdateSchema,
    IPAddressCreateSchema,
    IPAddressDetailSchema,
    IPAddressReadSchema,
    IPAddressUpdateSchema,
)

router = APIRouter()

# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session

# Create an IP address
@router.post("/", response_model=IPAddressReadSchema, status_code=status.HTTP_201_CREATED)
def create_ip_address(*, db: Session = Depends(get_db), ip_address_in: IPAddressCreateSchema):
    ip_address = IPAddress(ip_address=ip_address_in.ip_address)
    db.add(ip_address)
    db.commit()
    db.refresh(ip_address)
    return ip_address

# Get an IP address by ID
@router.get("/{ip_address_id}", response_model=IPAddressDetailSchema)
def read_ip_address(*, db: Session = Depends(get_db), ip_address_id: int):
    ip_address = db.get(IPAddress, ip_address_id)
    if not ip_address:
        raise HTTPException(status_code=404, detail="IP address not found")
    return ip_address

# Get a list of all IP addresses with optional filtering by city or country
@router.get("/", response_model=list[IPAddressReadSchema])
def read_ip_addresses(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    city_id: int | None,
    country_id: int | None
):
    query = select(IPAddress)

    # Apply filters if provided
    if city_id:
        query = query.where(IPAddress.city_id == city_id)
    if country_id:
        query = query.where(IPAddress.country_id == country_id)

    results = db.exec(query.offset(skip).limit(limit)).all()
    return results

# Update an IP address
@router.put("/{ip_address_id}", response_model=IPAddressReadSchema)
def update_ip_address(
    *,
    db: Session = Depends(get_db),
    ip_address_id: int,
    ip_address_in: IPAddressUpdateSchema
):
    ip_address = db.get(IPAddress, ip_address_id)
    if not ip_address:
        raise HTTPException(status_code=404, detail="IP address not found")

    # Update fields
    if ip_address_in.ip_address is not None:
        ip_address.ip_address = ip_address_in.ip_address

    db.add(ip_address)
    db.commit()
    db.refresh(ip_address)
    return ip_address

# Delete an IP address
@router.delete("/{ip_address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ip_address(*, db: Session = Depends(get_db), ip_address_id: int):
    ip_address = db.get(IPAddress, ip_address_id)
    if not ip_address:
        raise HTTPException(status_code=404, detail="IP address not found")

    db.delete(ip_address)
    db.commit()
    return None

# GeoLocation
@router.get("/", response_model=list[GeoLocationReadSchema])
async def get_all_geo_locations(session: Session = Depends(get_db)):
    locations = session.query(GeoLocation).all()
    return locations

@router.get("/{geo_location_id}", response_model=GeoLocationReadSchema)
async def get_geo_location(geo_location_id: uuid.UUID, session: Session = Depends(get_db)):
    location = session.get(GeoLocation, geo_location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GeoLocation not found")
    return location

@router.post("/", response_model=GeoLocationReadSchema, status_code=status.HTTP_201_CREATED)
async def create_geo_location(location_data: GeoLocationCreateSchema, session: Session = Depends(get_db)):
    location = GeoLocation.from_orm(location_data)
    session.add(location)
    session.commit()
    session.refresh(location)
    return location

@router.put("/{geo_location_id}", response_model=GeoLocationReadSchema)
async def update_geo_location(geo_location_id: uuid.UUID, location_data: GeoLocationUpdateSchema, session: Session = Depends(get_db)):
    location = session.get(GeoLocation, geo_location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GeoLocation not found")
    update_data = location_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(location, key, value)
    session.commit()
    session.refresh(location)
    return location

@router.delete("/{geo_location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_geo_location(geo_location_id: uuid.UUID, session: Session = Depends(get_db)):
    location = session.get(GeoLocation, geo_location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GeoLocation not found")
    session.delete(location)
    session.commit()
    return {"detail": "GeoLocation deleted"}

import uuid

from pydantic import BaseModel, IPvAnyAddress


# Define the schemas for related models (ASN, City, Country, etc.)
class AsnSchema(BaseModel):
    autonomous_system_number: int | None = None
    autonomous_system_organization: str | None = None
    ip_address: str | None = None
    network: str | None = None

    class Config:
        from_attributes = True

class CitySchema(BaseModel):
    geoname_id: int | None = None
    confidence: int | None = None
    name: str | None = None
    names: dict | None = None

    class Config:
        from_attributes = True

class CountrySchema(BaseModel):
    geoname_id: int | None = None
    confidence: str | None = None
    is_in_european_union: bool | None = None
    iso_code: str | None = None
    name: str | None = None
    names: dict | None = None

    class Config:
        from_attributes = True

class LocationSchema(BaseModel):
    accuracy_radius: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    metro_code: int | None = None
    time_zone: str | None = None

    class Config:
        from_attributes = True

class TraitsSchema(BaseModel):
    network: str | None = None

    class Config:
        from_attributes = True

class PostalSchema(BaseModel):
    confidence: int | None = None
    code: str | None = None

    class Config:
        from_attributes = True

class GeoLocationBase(BaseModel):
    continent: str | None = None  # Assuming a simple string here
    country: CountrySchema | None = None
    city: CitySchema | None = None
    location: LocationSchema | None = None
    asn: AsnSchema | None = None
    postal: PostalSchema | None = None

class GeoLocationCreateSchema(GeoLocationBase):
    pass

class GeoLocationUpdateSchema(BaseModel):
    city: str | None
    continent: str | None
    country: str | None
    latitude: float | None
    longitude: float | None
    postal_code: str | None

class GeoLocationReadSchema(GeoLocationBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

# Update IPAddress schemas
class IPAddressBase(BaseModel):
    ip_address: IPvAnyAddress

    class Config:
        from_attributes = True

class IPAddressCreateSchema(IPAddressBase):
    pass

class IPAddressUpdateSchema(IPAddressBase):
    ip_address: IPvAnyAddress | None = None

class IPAddressReadSchema(IPAddressBase):
    id: int
    city: CitySchema | None = None
    country: CountrySchema | None = None
    asn: AsnSchema | None = None
    location: LocationSchema | None = None
    traits: TraitsSchema | None = None

    class Config:
        from_attributes = True

class IPAddressDetailSchema(IPAddressReadSchema):
    geo_location: GeoLocationReadSchema | None = None  # Nested GeoLocation details

    class Config:
        from_attributes = True

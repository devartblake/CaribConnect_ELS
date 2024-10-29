from pydantic import BaseModel, IPvAnyAddress


# Define the schemas for related models (ASN, City, Country, etc.)
class ASNSchema(BaseModel):
    autonomous_system_number: int | None = None
    autonomous_system_organization: str | None = None
    ip_address: str | None = None
    network: str | None = None

    class Config:
        orm_mode = True

class CitySchema(BaseModel):
    geoname_id: int | None = None
    confidence: int | None = None
    name: str | None = None
    names: dict | None = None

    class Config:
        orm_mode = True

class CountrySchema(BaseModel):
    geoname_id: int | None = None
    confidence: str | None = None
    is_in_european_union: bool | None = None
    iso_code: str | None = None
    name: str | None = None
    names: dict | None = None

    class Config:
        orm_mode = True

class LocationSchema(BaseModel):
    accuracy_radius: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    metro_code: int | None = None
    time_zone: str | None = None

    class Config:
        orm_mode = True

class TraitsSchema(BaseModel):
    network: str | None = None

    class Config:
        orm_mode = True

class PostalSchema(BaseModel):
    confidence: int | None = None
    code: str | None = None

    class Config:
        orm_mode = True

class GeoLocationSchema(BaseModel):
    continent: str | None = None  # Assuming a simple string here
    country: CountrySchema | None = None
    city: CitySchema | None = None
    location: LocationSchema | None = None
    asn: ASNSchema | None = None
    postal: PostalSchema | None = None

    class Config:
        orm_mode = True

# Update IPAddress schemas
class IPAddressBase(BaseModel):
    ip_address: IPvAnyAddress

    class Config:
        orm_mode = True

class IPAddressCreateSchema(IPAddressBase):
    pass

class IPAddressUpdateSchema(IPAddressBase):
    ip_address: IPvAnyAddress | None = None

class IPAddressReadSchema(IPAddressBase):
    id: int
    city: CitySchema | None = None
    country: CountrySchema | None = None
    asn: ASNSchema | None = None
    location: LocationSchema | None = None
    traits: TraitsSchema | None = None

    class Config:
        orm_mode = True

class IPAddressDetailSchema(IPAddressReadSchema):
    geo_location: GeoLocationSchema | None = None  # Nested GeoLocation details

    class Config:
        orm_mode = True

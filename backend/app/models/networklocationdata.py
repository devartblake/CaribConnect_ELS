import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

# Define the GeoIP model components (like City, Country, etc.)
class Asn(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    autonomous_system_number: int | None
    autonomous_system_organization: str | None
    ip_address: str | None
    network: str | None = None

    # Relationship with IPAddress
    ip_addresses: list["IPAddress"] = Relationship(back_populates="asn")

class City(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    geoname_id: int | None
    confidence: int | None
    name: str | None
    names: dict[str, Any] | None = Field(sa_column=Column(JSON))

    # Relationship with IPAddress
    ip_addresses: list["IPAddress"] = Relationship(back_populates="city")

class Continent(SQLModel):
    geoname_id: int | None
    code: str | None
    name: str | None
    names: dict[str, Any] | None

class Country(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    geoname_id: int | None
    confidence: str | None
    is_in_european_union: bool | None
    iso_code: str | None
    name: str | None
    names: dict[str, Any] | None = Field(sa_column=Column(JSON))

    # Relationship with IPAddress
    ip_addresses: list["IPAddress"] = Relationship(back_populates="country")

class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    accuracy_radius: int | None
    latitude: float | None
    longitude: float | None
    metro_code: int | None
    time_zone: str | None

    # Relationship with IPAddress
    ip_addresses: list["IPAddress"] = Relationship(back_populates="location")

class Traits(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ip_addresses: list["IPAddress"] = Relationship(back_populates="traits")
    network: str | None = None

class Postal(SQLModel):
    confidence: int | None
    code: str | None

class GeoLocation(SQLModel):
    continent: Continent | None
    country: Country | None
    city: City | None
    location: Location | None
    asn: Asn | None
    postal: Postal | None

# Define the IPAddress model
class IPAddress(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ip_address: str = Field(max_length=45)  # Store IP as a string

    # Relationships to GeoIP models
    city_id: int | None = Field(default=None, foreign_key="city.id")
    city: City | None = Relationship(back_populates="ip_addresses")

    country_id: int | None = Field(default=None, foreign_key="country.id")
    country: Country | None = Relationship(back_populates="ip_addresses")
    asn_id: int | None = Field(default=None, foreign_key="asn.id")
    asn: Asn | None = Relationship(back_populates="ip_addresses")
    location_id: int | None = Field(default=None, foreign_key="location.id")
    location: Location | None = Relationship(back_populates="ip_addresses")
    # Example relationships to other models like GeoIP
    geoip_id: int | None = Field(default=None, foreign_key="geoip.id")
    geoip: Optional["GeoIP"] = Relationship(back_populates="ip_addresses")

    traits_id: int | None = Field(default=None, foreign_key="traits.id")
    traits: Optional["Traits"] = Relationship(back_populates="ip_addresses")

class IPAddressBase(SQLModel):
    ip: str

class IPAddressCreate(IPAddressBase):
    pass

class IPAddressUpdate(SQLModel):
    ip: str | None = None

class GeoIP(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ip_addresses: list["IPAddress"] = Relationship(back_populates="geoip")

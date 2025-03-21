from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class PropertyModel(BaseModel):
    propertyId: str = Field(alias='_id')
    title: str
    address: str
    cityId: str
    price: float
    bedrooms: int
    bathrooms: int
    status: str  # e.g., Available, Sold, Rented
    image: Optional[str] = None  # URL to property image

    @validator("propertyId", pre=True, always=True)
    def convert_objectId(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

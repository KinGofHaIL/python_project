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
        return v  # Fixed syntax issue here

    class Config:
        allow_population_by_field_name = True  # Allow using `_id` as `propertyId`
        json_encoders = {ObjectId: str}  # Ensure ObjectId is serialized properly

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from bson import ObjectId

class PropertyModel(BaseModel):
    propertyId: str = Field(alias='_id')
    title: str
    propertyName: str
    categoryId: str
    address: str
    cityId: str
    stateId: str
    zipcode: str
    areaId: str
    userId: str  # Owner (FK)
    description: Optional[str] = None
    basePrice: float
    otherPriceDescription: Optional[str] = None
    bedrooms: int
    bathrooms: int
    furnishingStatus: str  # e.g., Furnished, Semi-Furnished, Unfurnished
    yearBuilt: int
    status: str  # e.g., Available, Sold, Rented
    
    @validator("propertyId", pre=True, always=True)
    def convert_objectId(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

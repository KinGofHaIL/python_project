from pydantic import BaseModel
from typing import List, Optional

class PropertyDetailsModel(BaseModel):
    title: str
    address: str
    cityId: str
    price: float
    bedrooms: int
    bathrooms: int
    status: str
    description: Optional[str] = None
    features: Optional[List[str]] = []
    amenities: Optional[List[str]] = []

    class Config:
        from_attributes = True  # Fixes warning about `orm_mode`

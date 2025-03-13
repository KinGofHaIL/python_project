from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from models.PropertyModel import PropertyModel
from controllers import PropertyController

router = APIRouter()

@router.post("/create_property")
async def create_property(property: PropertyModel):
    return await PropertyController.create_property(property)

@router.post("/create_property_file")
async def create_property_with_file(
    title: str = Form(...),
    propertyName: str = Form(...),
    categoryId: str = Form(...),
    address: str = Form(...),
    cityId: str = Form(...),
    stateId: str = Form(...),
    zipcode: str = Form(...),
    areaId: str = Form(...),
    userId: str = Form(...),
    description: str = Form(...),
    basePrice: float = Form(...),
    otherPriceDescription: str = Form(...),
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    furnishingStatus: str = Form(...),
    yearBuilt: int = Form(...),
    status: str = Form(...),
    image: UploadFile = File(...)):
    return await PropertyController.create_property_with_file(
        title, propertyName, categoryId, address, cityId, stateId, zipcode, 
        areaId, userId, description, basePrice, otherPriceDescription, 
        bedrooms, bathrooms, furnishingStatus, yearBuilt, status, image
    )

@router.get("/get_properties")
async def get_properties():
    return await PropertyController.get_properties()

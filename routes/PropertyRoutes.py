from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from typing import Optional, List
from fastapi.responses import JSONResponse
from models.PropertyModel import PropertyModel
from controllers.PropertyController import PropertyController

router = APIRouter()

# ✅ Create Property (Without Image)
@router.post("/create_property", response_model=PropertyModel)
async def create_property(
    title: str = Form(...),
    address: str = Form(...),
    cityId: str = Form(...),
    price: float = Form(...),
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    status: str = Form(...)
):
    return await PropertyController.create_property({
        "title": title,
        "address": address,
        "cityId": cityId,
        "price": price,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "status": status,
        "image": None
    })

# ✅ Create Property (With Image Upload)
@router.post("/create_property_with_image", response_model=PropertyModel)
async def create_property_with_image(
    title: str = Form(...),
    address: str = Form(...),
    cityId: str = Form(...),
    price: float = Form(...),
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    status: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    image_url = None
    if image:
        # Save the image and get the URL (implement this logic)
        image_url = f"https://example.com/{image.filename}"
    return await PropertyController.create_property_with_image(
        title, address, cityId, price, bedrooms, bathrooms, status, image_url
    )

# ✅ Get All Properties
@router.get("/get_properties", response_model=List[PropertyModel])
async def get_properties():
    return await PropertyController.get_properties()

# ✅ Get Property by ID
@router.get("/get_property/{property_id}", response_model=PropertyModel)
async def get_property(property_id: str):
    return await PropertyController.get_property(property_id)

# ✅ Update Property
@router.put("/update_property/{property_id}", response_model=PropertyModel)
async def update_property(
    property_id: str,
    title: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    cityId: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    bedrooms: Optional[int] = Form(None),
    bathrooms: Optional[int] = Form(None),
    status: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    image_url = None
    if image:
        # Save the image and get the URL (implement this logic)
        image_url = f"https://example.com/{image.filename}"
    return await PropertyController.update_property(
        property_id, title, address, cityId, price, bedrooms, bathrooms, status, image_url
    )

# ✅ Delete Property
@router.delete("/delete_property/{property_id}")
async def delete_property(property_id: str):
    success = await PropertyController.delete_property(property_id)
    if success:
        return JSONResponse(content={"message": "Property deleted successfully"}, status_code=200)
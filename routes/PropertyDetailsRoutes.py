from fastapi import APIRouter, UploadFile, File, Form
from controllers.PropertyDetailsController import PropertyDetailsController

router = APIRouter()

# POST - Add property details (with image upload)
@router.post("/api/property-details/")
async def add_property_details(
    title: str = Form(...),
    address: str = Form(...),
    cityId: str = Form(...),
    price: float = Form(...),
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    status: str = Form(...),
    image: UploadFile = File(None)  # Optional image upload
):
    image_url = None
    if image:
        file_location = f"uploads/{image.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(image.file.read())
        image_url = file_location  # Save image URL in DB

    details = {
        "title": title,
        "address": address,
        "cityId": cityId,
        "price": price,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "status": status,
        "image": image_url
    }

    return await PropertyDetailsController.add_property_details(details)


# GET - Retrieve property details by ID
@router.get("/api/property-details/{property_id}")
async def get_property_details(property_id: str):
    return await PropertyDetailsController.get_property_details(property_id)

from models.PropertyModel import PropertyModel
from config.database import property_collection, category_collection, user_collection, city_collection, state_collection, area_collection
from fastapi import HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from bson import ObjectId
import shutil
import os
from utils.CloudinaryUtil import upload_image

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def create_property(property: PropertyModel):
    property.categoryId = ObjectId(property.categoryId)
    property.cityId = ObjectId(property.cityId)
    property.stateId = ObjectId(property.stateId)
    property.areaId = ObjectId(property.areaId)
    property.userId = ObjectId(property.userId)
    
    saved_property = await property_collection.insert_one(property.dict())
    return JSONResponse(content={"message": "Property created successfully"}, status_code=201)

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
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_ext = image.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_DIR, f"{ObjectId()}.{file_ext}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = await upload_image(file_path)
        
        property_data = {
            "title": title,
            "propertyName": propertyName,
            "categoryId": str(ObjectId(categoryId)),
            "address": address,
            "cityId": str(ObjectId(cityId)),
            "stateId": str(ObjectId(stateId)),
            "zipcode": zipcode,
            "areaId": str(ObjectId(areaId)),
            "userId": str(ObjectId(userId)),
            "description": description,
            "basePrice": basePrice,
            "otherPriceDescription": otherPriceDescription,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "furnishingStatus": furnishingStatus,
            "yearBuilt": yearBuilt,
            "status": status,
            "image_url": image_url
        }
        
        await property_collection.insert_one(property_data)
        return JSONResponse(content={"message": "Property created successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

async def get_properties():
    try:
        properties = await property_collection.find().to_list(None)
        
        def convert_objectid_to_str(data):
            if isinstance(data, ObjectId):
                return str(data)
            elif isinstance(data, dict):
                return {k: convert_objectid_to_str(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [convert_objectid_to_str(i) for i in data]
            return data
        
        for prop in properties:
            prop["_id"] = str(prop["_id"])
            prop["categoryId"] = str(prop["categoryId"])
            prop["cityId"] = str(prop["cityId"])
            prop["stateId"] = str(prop["stateId"])
            prop["areaId"] = str(prop["areaId"])
            prop["userId"] = str(prop["userId"])
            
            category = await category_collection.find_one({"_id": ObjectId(prop["categoryId"])});
            if category:
                prop["category"] = convert_objectid_to_str(category)
            
            city = await city_collection.find_one({"_id": ObjectId(prop["cityId"])});
            if city:
                prop["city"] = convert_objectid_to_str(city)
            
            state = await state_collection.find_one({"_id": ObjectId(prop["stateId"])});
            if state:
                prop["state"] = convert_objectid_to_str(state)
            
            area = await area_collection.find_one({"_id": ObjectId(prop["areaId"])});
            if area:
                prop["area"] = convert_objectid_to_str(area)
            
            user = await user_collection.find_one({"_id": ObjectId(prop["userId"])});
            if user:
                prop["user"] = convert_objectid_to_str(user)
        
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching properties")
from models.PropertyModel import PropertyModel
from typing import List, Optional
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.real_estate_db
properties_collection = db.properties

class PropertyController:
    @staticmethod
    async def create_property(property_data: dict) -> PropertyModel:
        try:
            # Insert property into MongoDB
            result = await properties_collection.insert_one(property_data)
            if result.inserted_id:
                property_data["_id"] = str(result.inserted_id)  # Convert to string
                return PropertyModel(**property_data)
            raise HTTPException(status_code=500, detail="Failed to create property")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def create_property_with_image(
        title: str, address: str, cityId: str, price: float, bedrooms: int, bathrooms: int, status: str, image: Optional[str]
    ) -> PropertyModel:
        try:
            property_data = {
                "title": title,
                "address": address,
                "cityId": cityId,
                "price": price,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "status": status,
                "image": image
            }
            return await PropertyController.create_property(property_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_properties() -> List[dict]:
        try:
            properties = []
            async for property in properties_collection.find():
                property["_id"] = str(property["_id"])  # Convert ObjectId to string
                properties.append(property)
            return properties
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_property(property_id: str) -> dict:
        try:
            obj_id = ObjectId(property_id)  # Ensure valid ObjectId
        except:
            raise HTTPException(status_code=400, detail="Invalid property ID format")

        property = await properties_collection.find_one({"_id": obj_id})
        if property:
            property["_id"] = str(property["_id"])  # Convert ObjectId to string
            return property
        raise HTTPException(status_code=404, detail="Property not found")

    @staticmethod
    async def update_property(
        property_id: str, title: Optional[str], address: Optional[str], cityId: Optional[str], price: Optional[float],
        bedrooms: Optional[int], bathrooms: Optional[int], status: Optional[str], image: Optional[str]
    ) -> dict:
        try:
            obj_id = ObjectId(property_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid property ID format")

        update_data = {}
        if title:
            update_data["title"] = title
        if address:
            update_data["address"] = address
        if cityId:
            update_data["cityId"] = cityId
        if price:
            update_data["price"] = price
        if bedrooms:
            update_data["bedrooms"] = bedrooms
        if bathrooms:
            update_data["bathrooms"] = bathrooms
        if status:
            update_data["status"] = status
        if image:
            update_data["image"] = image

        result = await properties_collection.update_one(
            {"_id": obj_id}, {"$set": update_data}
        )
        if result.modified_count > 0:
            updated_property = await properties_collection.find_one({"_id": obj_id})
            updated_property["_id"] = str(updated_property["_id"])  # Convert ObjectId to string
            return updated_property
        raise HTTPException(status_code=404, detail="Property not found")

    @staticmethod
    async def delete_property(property_id: str) -> bool:
        try:
            obj_id = ObjectId(property_id)  # Ensure valid ObjectId
        except:
            raise HTTPException(status_code=400, detail="Invalid property ID format")

        result = await properties_collection.delete_one({"_id": obj_id})
        if result.deleted_count > 0:
            return True
        raise HTTPException(status_code=404, detail="Property not found")

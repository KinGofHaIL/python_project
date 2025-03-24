from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from bson import ObjectId
from models.PropertyDetailsModel import PropertyDetailsModel

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.real_estate_db
properties_collection = db.properties
property_details_collection = db.property_details

class PropertyDetailsController:
    @staticmethod
    async def add_property_details(property_id: str, details: dict) -> PropertyDetailsModel:
        try:
            print(f"🔍 Checking Property ID: {property_id}")  # Debug log
            existing_details = await property_details_collection.find_one({"property_id": property_id})
            
            if existing_details:
                print("ℹ️ Updating existing property details")  # Debug log
                await property_details_collection.update_one(
                    {"property_id": property_id}, {"$set": details}
                )
            else:
                print("➕ Adding new property details")  # Debug log
                details["property_id"] = property_id
                await property_details_collection.insert_one(details)

            updated_details = await property_details_collection.find_one({"property_id": property_id})
            if updated_details:
                updated_details.pop("_id", None)  # Remove MongoDB's _id field

            return PropertyDetailsModel(**updated_details)

        except Exception as e:
            print(f"💥 Unexpected Error: {str(e)}")  # Debug log
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_property_details(property_id: str) -> dict:
        try:
            print(f"🔍 Fetching Property ID: {property_id}")  # Debug log
            if not ObjectId.is_valid(property_id):
                print("❌ Invalid Property ID format!")  # Debug log
                raise HTTPException(status_code=400, detail="Invalid Property ID format")

            # Fetch basic property info from properties collection
            property_data = await properties_collection.find_one({"_id": ObjectId(property_id)})
            if not property_data:
                print("❌ Property not found!")  # Debug log
                raise HTTPException(status_code=404, detail="Property not found")

            property_data["_id"] = str(property_data["_id"])  # Convert ObjectId to string

            # Fetch additional details from property_details collection
            details_data = await property_details_collection.find_one({"property_id": property_id})
            if details_data:
                details_data.pop("_id", None)  # Remove MongoDB's _id field
                property_data.update(details_data)  # Merge details into property data

            return property_data

        except HTTPException as http_exc:
            print(f"⚠️ FastAPI HTTP Exception: {http_exc.detail}")  # Debug log
            raise http_exc  # Preserve FastAPI HTTP exceptions
        except Exception as e:
            print(f"💥 Unexpected Error: {str(e)}")  # Debug log
            raise HTTPException(status_code=500, detail=str(e))

from models.AreaModel import Area, AreaOut
from bson import ObjectId
from config.database import area_collection, city_collection
from fastapi.responses import JSONResponse

async def addArea(area: Area):
    saved_area = await area_collection.insert_one(area.dict())
    return JSONResponse(content={"message": "Area added successfully"}, status_code=201)

async def getArea():
    areas = await area_collection.find().to_list(length=100)  # Specify length

    for area in areas:
        if "city_id" in area and isinstance(area["city_id"], ObjectId):
            area["city_id"] = str(area["city_id"])  # Convert ObjectId to string

        city = await city_collection.find_one({"_id": ObjectId(area["city_id"])}) if "city_id" in area else None
        
        if city:
            city["_id"] = str(city["_id"])  # Convert city _id to string
            area["city"] = city  # Attach city data to the area

    return [AreaOut(**area) for area in areas]

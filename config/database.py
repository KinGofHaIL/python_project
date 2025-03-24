from motor.motor_asyncio import AsyncIOMotorClient

# Database connection settings
MONGO_URL = "mongodb://localhost:27017"
DATABASE_NAME = "real_estate_db"  # Ensure this matches across all files

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

# Collections
role_collection = db["roles"]
user_collection = db["users"]
state_collection = db["states"]
city_collection = db["cities"]
area_collection = db["areas"]
agent_collection = db["agents"]
category_collection = db["categories"]
sub_category_collection = db["sub_categories"]
# product_collection = db["products"]
property_details_collection = db["property_details"]  # Consistent with PropertyDetailsController.py
properties_collection = db["properties"]

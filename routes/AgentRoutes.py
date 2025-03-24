from fastapi import APIRouter, HTTPException
from config.database import agent_collection, state_collection, city_collection, area_collection
from models.AgentModel import Agent
from bson import ObjectId

router = APIRouter()

def to_object_id(value):
    try:
        return ObjectId(value) if value and ObjectId.is_valid(value) else None
    except:
        return None

# ✅ **1. Add Agent**
@router.post("/agent/add")
async def add_agent(agent: Agent):
    try:
        # Convert to dictionary
        agent_data = agent.dict()
        
        # Fetch and store state details
        state = await state_collection.find_one({"_id": to_object_id(agent_data.get("state_id"))})
        agent_data["state"] = {"id": str(state["_id"]), "name": state["name"]} if state else {}
        
        # Fetch and store city details
        city = await city_collection.find_one({"_id": to_object_id(agent_data.get("city_id"))})
        agent_data["city"] = {"id": str(city["_id"]), "name": city["name"]} if city else {}
        
        # Fetch and store area details
        area = await area_collection.find_one({"_id": to_object_id(agent_data.get("area_id"))})
        agent_data["area"] = {"id": str(area["_id"]), "name": area["name"]} if area else {}
        
        # Remove old ID references
        agent_data.pop("state_id", None)
        agent_data.pop("city_id", None)
        agent_data.pop("area_id", None)
        
        # Insert into MongoDB
        saved_agent = await agent_collection.insert_one(agent_data)

        if not saved_agent.inserted_id:
            raise HTTPException(status_code=500, detail="❌ Failed to add agent")

        return {"message": "✅ Agent added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ **2. Get All Agents (With State, City, and Area Details)**
@router.get("/agents")
async def get_agents():
    agents = await agent_collection.find().to_list(length=100)
    
    agent_list = []
    for agent in agents:
        agent_list.append({
            "agentName": agent.get("name", "N/A"),  # Use correct field name
            "agencyName": agent.get("agencyName", "Private"),
            "experience": agent.get("experience", 0),
            "contactNo": agent.get("contact_no", "N/A"),
            "email": agent.get("email", "N/A"),
            "state": agent.get("state", {}),
            "city": agent.get("city", {}),
            "area": agent.get("area", {})
        })
    
    return agent_list
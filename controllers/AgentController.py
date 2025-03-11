from models.AgentModel import Agent, AgentOut
from bson import ObjectId
from config.database import agent_collection, state_collection, city_collection, area_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse


# ✅ **1. Add Agent**
async def addAgent(agent: Agent):
    try:
        # Convert string IDs to ObjectId
        agent.state_id = ObjectId(agent.state_id) if agent.state_id else None
        agent.city_id = ObjectId(agent.city_id) if agent.city_id else None
        agent.area_id = ObjectId(agent.area_id) if agent.area_id else None

        # Insert into MongoDB
        saved_agent = await agent_collection.insert_one(agent.dict())

        if not saved_agent.inserted_id:
            raise HTTPException(status_code=500, detail="❌ Failed to add agent")

        return JSONResponse(content={"message": "✅ Agent added successfully"}, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ **2. Get All Agents (With State, City, and Area Details)**
async def getAgents():
    agents = await agent_collection.find().to_list(length=100)

    for agent in agents:
        # Convert ObjectId fields to string
        agent["_id"] = str(agent["_id"])
        agent["state_id"] = str(agent["state_id"]) if "state_id" in agent else None
        agent["city_id"] = str(agent["city_id"]) if "city_id" in agent else None
        agent["area_id"] = str(agent["area_id"]) if "area_id" in agent else None

        # Fetch state details
        if agent.get("state_id"):
            state = await state_collection.find_one({"_id": ObjectId(agent["state_id"])})
            agent["state"] = {"_id": str(state["_id"]), "name": state["name"]} if state else None

        # Fetch city details
        if agent.get("city_id"):
            city = await city_collection.find_one({"_id": ObjectId(agent["city_id"])})
            agent["city"] = {"_id": str(city["_id"]), "name": city["name"]} if city else None

        # Fetch area details
        if agent.get("area_id"):
            area = await area_collection.find_one({"_id": ObjectId(agent["area_id"])})
            agent["area"] = {"_id": str(area["_id"]), "name": area["name"]} if area else None

    return [AgentOut(**agent) for agent in agents]

from fastapi import APIRouter
from config.database import agent_collection
from models.AgentModel import Agent, AgentOut
from bson import ObjectId

router = APIRouter()

# Add agent
@router.post("/agent/add")
async def add_agent(agent: Agent):
    saved_agent = await agent_collection.insert_one(agent.dict())
    return {"message": "Agent added successfully"}

# Get all agents
@router.get("/agents")
async def get_agents():
    agents = await agent_collection.find().to_list(length=100)
    return [{"id": str(agent["_id"]), "name": agent["agencyName"], "experience": agent["experience"]} for agent in agents]

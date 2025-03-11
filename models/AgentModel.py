from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

# Helper function to convert ObjectId
def to_object_id(value):
    if isinstance(value, str):
        return ObjectId(value)
    return value

class State(BaseModel):
    id: str = Field(alias="_id")
    name: str

    @validator("id", pre=True, always=True)
    def convert_state_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

class City(BaseModel):
    id: str = Field(alias="_id")
    name: str

    @validator("id", pre=True, always=True)
    def convert_city_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

class Area(BaseModel):
    id: str = Field(alias="_id")
    name: str

    @validator("id", pre=True, always=True)
    def convert_area_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

class Agent(BaseModel):
    agentId: str
    agencyName: str
    experience: int
    userId: str
    state: State
    city: Optional[City] = None
    area: Optional[Area] = None

    @validator("userId", pre=True, always=True)
    def convert_user_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

class AgentOut(Agent):
    id: str = Field(alias="_id")

    @validator("id", pre=True, always=True)
    def convert_objectId(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

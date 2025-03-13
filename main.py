from fastapi import FastAPI
from routes.RoleRoutes import router as role_router
from routes.UserRoutes import router as user_router
from routes.StateRoutes import router as state_router
from routes.CityRoutes import router as city_router
from routes.AreaRoutes import router as area_router
from routes.AgentRoutes import router as agent_router  # Added agent routes
from fastapi.middleware.cors import CORSMiddleware
from config.database import user_collection
from routes.CategoryRoutes import router as category_router
from routes.SubCategoryRoutes import router as sub_category_router
from routes.ProductRoutes import router as product_router
from routes.PropertyRoutes import router as property_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(role_router)
app.include_router(user_router)
app.include_router(state_router)
app.include_router(city_router)
app.include_router(area_router)
app.include_router(agent_router)  # Added agent routes
app.include_router(category_router)
app.include_router(sub_category_router)
app.include_router(product_router)
app.include_router(property_router)

# Get all users
@app.get("/users")
async def get_users():
    users = await user_collection.find().to_list(length=100)
    return [{"id": str(user["_id"]), "name": user["name"], "email": user["email"]} for user in users]

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

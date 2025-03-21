from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config.database import user_collection

# Import routes
from routes.RoleRoutes import router as role_router
from routes.UserRoutes import router as user_router
from routes.StateRoutes import router as state_router
from routes.CityRoutes import router as city_router
from routes.AreaRoutes import router as area_router
from routes.AgentRoutes import router as agent_router
from routes.CategoryRoutes import router as category_router
from routes.SubCategoryRoutes import router as sub_category_router
from routes.ProductRoutes import router as product_router
from routes.PropertyRoutes import router as property_router

# ✅ Create FastAPI app
app = FastAPI(
    title="Real Estate API",
    version="1.0.0",
    description="API for managing real estate properties, users, and related entities.",
    docs_url="/docs",  # Enable Swagger UI at /docs
    redoc_url="/redoc",  # Enable ReDoc at /redoc
)

# ✅ Allow frontend to access API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ✅ Serve static files (Property Images)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Include API routes
app.include_router(role_router, prefix="/api/roles", tags=["Roles"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(state_router, prefix="/api/states", tags=["States"])
app.include_router(city_router, prefix="/api/cities", tags=["Cities"])
app.include_router(area_router, prefix="/api/areas", tags=["Areas"])
app.include_router(agent_router, prefix="/api/agents", tags=["Agents"])
app.include_router(category_router, prefix="/api/categories", tags=["Categories"])
app.include_router(sub_category_router, prefix="/api/subcategories", tags=["Subcategories"])
app.include_router(product_router, prefix="/api/products", tags=["Products"])
app.include_router(property_router, prefix="/api/properties", tags=["Properties"])

# ✅ Server health check
@app.get("/", tags=["Root"])
async def root():
    return {"message": "🏡 Real Estate API is running!"}

# ✅ Get all users
@app.get("/users", tags=["Users"])
async def get_users():
    try:
        users = await user_collection.find().to_list(length=100)
        return [{"id": str(user["_id"]), "name": user["name"], "email": user["email"]} for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ✅ Server lifecycle events
@app.on_event("startup")
async def startup_event():
    print("🚀 Server is starting...")

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Server is shutting down...")

# ✅ Run the server using the command below:
# python -m uvicorn main:app --reload
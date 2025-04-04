from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config.database import user_collection
import logging

# Import routes
from routes.RoleRoutes import router as role_router
from routes.UserRoutes import router as user_router
from routes.StateRoutes import router as state_router
from routes.CityRoutes import router as city_router
from routes.AreaRoutes import router as area_router
from routes.AgentRoutes import router as agent_router
from routes.CategoryRoutes import router as category_router
from routes.SubCategoryRoutes import router as sub_category_router
# from routes.ProductRoutes import router as product_router
from routes.PropertyRoutes import router as property_router
from routes.PropertyDetailsRoutes import router as property_details_router
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes import profile  # Import the profile route
from routes.profile import router as profile_router
from routes.auth_routes import router as auth_router
from routes.profile_routes import router as profile_router  # ✅ Import profile routes

app = FastAPI()

# Include routes
app.include_router(profile.router)


# ✅ Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Create FastAPI app
app = FastAPI(
    title="Real Estate API",
    version="1.0.0",
    description="API for managing real estate properties, users, and related entities.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ✅ Allow frontend to access API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
# app.include_router(product_router, prefix="/api/products", tags=["Products"])
app.include_router(property_router, prefix="/api/properties", tags=["Properties"])
app.include_router(property_details_router)
app.include_router(auth_router)
app.include_router(user_router, prefix="/api/users")
app.include_router(profile.router)
app.include_router(profile_router, prefix="/api", tags=["Profile"])
app.include_router(auth_router)  # ✅ Authentication Routes
app.include_router(profile_router)  # ✅ Profile Routes



# ✅ Server health check
@app.get("/", tags=["Root"])
async def root():
    return {"message": "🏡 Real Estate API is running!"}

# ✅ Get all users
@app.get("/users", tags=["Users"])
async def get_users():
    try:
        users = await user_collection.find().to_list(length=100)
        return [
            {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
            for user in users
        ]
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred.")

# ✅ Server lifecycle events
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("🚀 Server is starting...")
        # You can add database connection validation here
    except Exception as e:
        logger.error(f"Error during startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    try:
        logger.info("🛑 Server is shutting down...")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# ✅ Run the server using:
# python -m uvicorn main:app --reload


@app.get("/")
def home():
    return {"message": "Real Estate API Running"}

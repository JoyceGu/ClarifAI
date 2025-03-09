from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import Base, engine
from .models.models import User
from .auth import get_password_hash
from .routers import auth, requirements

app = FastAPI(title="ClarifAI - Requirement Management System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="app/templates")

# Include routers with prefix
app.include_router(auth.router, prefix="/api", tags=["authentication"])
app.include_router(requirements.router, prefix="/api", tags=["requirements"])

@app.on_event("startup")
async def startup():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create test accounts if they don't exist
    async with AsyncSession(engine) as session:
        # Check if PM account exists
        result = await session.execute(select(User).filter(User.email == "pm@test.com"))
        pm_user = result.scalar_one_or_none()
        if not pm_user:
            # Create PM test account
            pm_user = User(
                email="pm@test.com",
                hashed_password=get_password_hash("password123"),
                role="pm",
                is_active=True
            )
            session.add(pm_user)
        
        # Check if Researcher account exists
        result = await session.execute(select(User).filter(User.email == "researcher@test.com"))
        researcher_user = result.scalar_one_or_none()
        if not researcher_user:
            # Create Researcher test account
            researcher_user = User(
                email="researcher@test.com",
                hashed_password=get_password_hash("password123"),
                role="researcher",
                is_active=True
            )
            session.add(researcher_user)
        
        # Commit changes if any accounts were created
        await session.commit()
        
    print("Database initialized with test accounts")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/all-tasks")
async def all_tasks(request: Request):
    return templates.TemplateResponse("all_tasks.html", {"request": request})

@app.get("/task-detail/{task_id}")
async def task_detail(request: Request, task_id: int):
    return templates.TemplateResponse("task_detail.html", {"request": request, "task_id": task_id}) 
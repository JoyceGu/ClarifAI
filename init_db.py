import asyncio
from app.database import engine, Base
from app.models.models import User
from app.auth import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def init_db():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Create test users
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        # Create PM user
        pm_user = User(
            email="pm@test.com",
            hashed_password=get_password_hash("password123"),
            role="pm"
        )
        session.add(pm_user)
        
        # Create researcher user
        researcher_user = User(
            email="researcher@test.com",
            hashed_password=get_password_hash("password123"),
            role="researcher"
        )
        session.add(researcher_user)
        
        await session.commit()

if __name__ == "__main__":
    asyncio.run(init_db()) 
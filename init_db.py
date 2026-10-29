import asyncio
from app.core.database import engine, Base, AsyncSessionLocal
from app.services.seeder import seed_database

async def init():
    print("Creating tables in PostgreSQL truthin_db...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Seeding initial products, additives, and default profile...")
    async with AsyncSessionLocal() as session:
        await seed_database(session)
        
    await engine.dispose()
    print("Database initialization complete!")

if __name__ == "__main__":
    asyncio.run(init())

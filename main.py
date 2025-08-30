from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
import os
from contextlib import asynccontextmanager

from database import engine, get_db
from models import Base
from routers import auth, apis, ai_search, analytics
from auth import get_current_user

# Create database tables on startup

@asynccontextmanager
async def lifespan(app: FastAPI):
# Startup
async with engine.begin() as conn:
await conn.run_sync(Base.metadata.create_all)

```
# Connect to Redis
app.state.redis = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379")
)

yield

# Shutdown
await app.state.redis.close()
```

app = FastAPI(
title=“AI API Platform”,
description=“AI-powered API discovery and integration platform”,
version=“1.0.0”,
lifespan=lifespan
)

# CORS middleware

app.add_middleware(
CORSMiddleware,
allow_origins=[”*”],  # Configure for production
allow_credentials=True,
allow_methods=[”*”],
allow_headers=[”*”],
)

# Include routers

app.include_router(auth.router, prefix=”/auth”, tags=[“authentication”])
app.include_router(apis.router, prefix=”/apis”, tags=[“api-management”])
app.include_router(ai_search.router, prefix=”/ai”, tags=[“ai-search”])
app.include_router(analytics.router, prefix=”/analytics”, tags=[“analytics”])

@app.get(”/”)
async def root():
return {“message”: “AI API Platform is running!”, “status”: “healthy”}

@app.get(”/health”)
async def health_check(db: AsyncSession = Depends(get_db)):
try:
# Test database connection
result = await db.execute(“SELECT 1”)

```
    # Test Redis connection
    await app.state.redis.ping()
    
    return {"status": "healthy", "database": "connected", "redis": "connected"}
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
```
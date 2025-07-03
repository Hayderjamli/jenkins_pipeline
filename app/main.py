from fastapi import FastAPI
from sqlalchemy.sql import text
from app.services.database import SessionLocal, init_db
from app.services.redis_client import get_redis
from app.services.elasticsearch_client import get_elasticsearch
from app.api.v1 import router as v1_router
from starlette.responses import Response
import os
import redis
# app/main.py
from prometheus_client import Counter, start_http_server,generate_latest
if not os.getenv("TESTING"):
    start_http_server(8002)  # Only start if not in test mode
app = FastAPI()

REQUEST_COUNT = Counter('request_count', 'Total request count')
@app.get("/")
async def read_root():
    return {"message": "Hello World"}
@app.get("/metrics")
async def metrics():
    REQUEST_COUNT.inc()
    return Response(generate_latest(REQUEST_COUNT), media_type="text/plain")

@app.on_event("startup")
async def startup_event():
    init_db()
    # Test connections
    try:
        redis_client = get_redis()
        redis_client.ping()
        app.state.redis_status = "Redis connection successful"
    except redis.ConnectionError:
        app.state.redis_status = "Redis connection failed"
    
    try:
        es_client = get_elasticsearch()
        es_client.ping()
        app.state.es_status = "Elasticsearch connection successful"
    except Exception:
        app.state.es_status = "Elasticsearch connection failed"
    
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        app.state.db_status = "PostgreSQL connection successful"
    finally:
        db.close()

@app.get("/health")
async def health_check():
    return {
        "redis": app.state.redis_status,
        "elasticsearch": app.state.es_status,
        "postgresql": app.state.db_status
    }

# Include API v1 router
app.include_router(v1_router)

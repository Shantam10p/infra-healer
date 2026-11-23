import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from backend.db import get_connection
from backend.orders import router as orders_router
from backend.redis_client import redis_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("api")

app = FastAPI()
app.include_router(orders_router)

APP_NAME = os.getenv("APP_NAME", "phase1-api")

@app.get("/")
def root(): 
  logger.info("root endpoint called")
  return {"message": "hello from {APP_NAME}"}

@app.get("/health")
def health():
  checks = {}

  try:
    with get_connection() as conn:
      conn.execute("SELECT 1")
    checks["postgres"] = "ok"
  except Exception:
    checks["postgres"] = "down"

  try:
    redis_client.ping()
    checks["redis"] = "ok"
  except Exception:
    checks["redis"] = "down"

  if "down" in checks.values():
    return JSONResponse(status_code=503, content={"status": "unhealthy", **checks})
  return {"status": "ok", **checks}

@app.get("/error")
def error():
  logger.error("somethig went wrong on purpose")
  raise HTTPException(status_code = 500, detail= "intentional error")
 
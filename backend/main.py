import logging
import os
from fastapi import FastAPI, HTTPException
from backend.orders import router as orders_router

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
  return {"status": "ok"}

@app.get("/error")
def error():
  logger.error("somethig went wrong on purpose")
  raise HTTPException(status_code = 500, detail= "intentional error")
 
from fastapi import APIRouter
from backend.db import get_connection

router = APIRouter()

@router.get("/menu")
def get_menu():
  with get_connection() as conn:
    rows = conn.execute("SELECT * FROM menu").fetchall()
  return rows


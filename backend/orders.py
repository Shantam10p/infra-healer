from fastapi import APIRouter, HTTPException
from backend.db import get_connection
from backend.schemas.orders import OrderIn

router = APIRouter()

@router.get("/menu")
def get_menu():
  with get_connection() as conn:
    rows = conn.execute("SELECT * FROM menu").fetchall()
  return rows

@router.post("/order")
def post_order(order: OrderIn):
  with get_connection() as conn:
    new_order = conn.execute("INSERT INTO orders (first_name, last_name) VALUES (%s, %s) RETURNING id",(order.first_name, order.last_name)
    ).fetchone()

    for item in order.items:
      menu_row = conn.execute(
        "SELECT price FROM menu WHERE id = %s", (item.drink_id,)
      ).fetchone()

      if menu_row is None:
        raise HTTPException(status_code=404, detail=f"Drink {item.drink_id} not found")

      conn.execute(
        "INSERT INTO order_items (order_id, drink_id, size, sugar, quantity, price) VALUES (%s, %s, %s, %s, %s, %s)",
        (new_order["id"], item.drink_id, item.size, item.sugar, item.quantity, menu_row["price"]),
      )

  return new_order





 

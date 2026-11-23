from pydantic import BaseModel

class OrderItemIn(BaseModel):
  drink_id: int
  size: str
  sugar: bool = False
  quantity: int


class OrderIn(BaseModel):
  first_name: str
  last_name: str | None = None
  items: list[OrderItemIn]


  
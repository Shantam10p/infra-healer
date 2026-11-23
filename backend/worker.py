import time

from backend.db import get_connection
from backend.redis_client import redis_client

while True:
    redis_client.set("worker:heartbeat", int(time.time()))

    job = redis_client.brpop("orders", 5)
    if job is None:
        continue
    _, order_id = job

    with get_connection() as conn:
        conn.execute("UPDATE orders SET status = 'processing' WHERE id = %s", (order_id,))

    time.sleep(3)

    with get_connection() as conn:
        conn.execute("UPDATE orders SET status = 'ready' WHERE id = %s", (order_id,))

import time

from prometheus_client import Counter, Histogram, start_http_server

from backend.db import get_connection
from backend.redis_client import redis_client

orders_processed = Counter("orders_processed_total", "Orders the worker finished")
order_processing_seconds = Histogram("order_processing_seconds", "Time taken to process an order")

start_http_server(8001)

while True:
    redis_client.set("worker:heartbeat", int(time.time()))

    job = redis_client.brpop("orders", 5)
    if job is None:
        continue
    _, order_id = job

    with order_processing_seconds.time():
        with get_connection() as conn:
            conn.execute("UPDATE orders SET status = 'processing' WHERE id = %s", (order_id,))

        time.sleep(3)

        with get_connection() as conn:
            conn.execute("UPDATE orders SET status = 'ready' WHERE id = %s", (order_id,))

    orders_processed.inc()

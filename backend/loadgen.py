import json
import random
import time
import urllib.request

API_URL = "http://api:8000/order"
NAMES = ["Alex", "Sam", "Priya", "Lee", "Kai", "Maya"]
SIZES = ["small", "medium", "large"]

while True:
    order = {
        "first_name": random.choice(NAMES),
        "items": [
            {
                "drink_id": random.randint(1, 4),
                "size": random.choice(SIZES),
                "sugar": random.choice([True, False]),
                "quantity": random.randint(1, 3),
            }
        ],
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(order).encode(),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(request) as response:
            print("order placed:", json.load(response), flush=True)
    except Exception as error:
        print("order failed:", error, flush=True)

    time.sleep(30)

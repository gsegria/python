import time
import random

start_time = time.time()

def get_engineering_data():

    t = time.time() - start_time

    return {
        "time": round(t, 2),
        "temperature": round(40 + random.uniform(-5, 5), 2),
        "voltage": round(12 + random.uniform(-0.3, 0.3), 2),
        "speed": round(5 + random.uniform(-1, 1), 2)
    }
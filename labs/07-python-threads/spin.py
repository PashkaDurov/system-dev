import os
import threading
import time

def occupy_processor():
    deadline = time.perf_counter() + 15
    while time.perf_counter() < deadline:
        pass

print('pid:', os.getpid(), flush=True)
workers = [threading.Thread(target=occupy_processor) for _ in range(4)]
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()

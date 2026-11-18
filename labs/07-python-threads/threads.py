"""Одинаковый объём вычислений при разном количестве потоков."""
import json
import os
import sys
import threading
import time

WORK_UNITS = 200_000_000

def calculate(portion):
    accumulator = 0
    for position in range(portion):
        accumulator += 1
    assert accumulator == portion

print(json.dumps({'python': sys.version, 'gil': sys._is_gil_enabled(), 'pid': os.getpid()}), flush=True)
for worker_count in (1, 2, 4):
    workers = [threading.Thread(target=calculate, args=(WORK_UNITS // worker_count,))
               for _ in range(worker_count)]
    beginning = time.perf_counter()
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    print(json.dumps({'workers': worker_count, 'seconds': time.perf_counter() - beginning}), flush=True)

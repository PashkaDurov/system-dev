import threading
import time

for worker_count in (1, 4):
    workers = [threading.Thread(target=time.sleep, args=(2,)) for _ in range(worker_count)]
    beginning = time.perf_counter()
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    print(f'{worker_count} workers: {time.perf_counter() - beginning:.3f} seconds')

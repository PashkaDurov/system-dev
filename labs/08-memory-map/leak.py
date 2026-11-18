import os
import time

print('PID:', os.getpid(), flush=True)
retained_chunks = []
for second in range(60):
    retained_chunks.append(bytearray(10 * 1024 * 1024))
    print('retained MiB:', (second + 1) * 10, flush=True)
    time.sleep(1)

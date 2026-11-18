"""Переходы между этапами: Enter; удобно снимать карту памяти."""
import mmap
import os

print('PID:', os.getpid(), flush=True)
input('Start: Enter to allocate 300 MiB ')
region = mmap.mmap(-1, 300 * 1024 * 1024)
input('Allocated: Enter to touch every page ')
for offset in range(0, len(region), mmap.PAGESIZE):
    region[offset] = 1
input('Touched: Enter to release ')
region.close()
input('Released: Enter to exit ')

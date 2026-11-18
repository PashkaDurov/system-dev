import ctypes
import faulthandler

ctypes.windll.kernel32.SetErrorMode(3)
faulthandler.enable()

def write_bytes(destination):
    ctypes.memset(destination, 0, 8)

print('Writing eight bytes to NULL', flush=True)
write_bytes(0)

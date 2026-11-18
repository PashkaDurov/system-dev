import ctypes
import os

def modules():
    from ctypes import wintypes
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.K32EnumProcessModules.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.HMODULE), wintypes.DWORD, ctypes.POINTER(wintypes.DWORD))
    kernel.K32GetModuleFileNameExW.argtypes = (wintypes.HANDLE, wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD)
    proc = kernel.GetCurrentProcess()
    handles = (wintypes.HMODULE * 1024)()
    needed = wintypes.DWORD()
    if not kernel.K32EnumProcessModules(proc, handles, ctypes.sizeof(handles), ctypes.byref(needed)):
        raise ctypes.WinError(ctypes.get_last_error())
    paths = []
    for handle in handles[:needed.value // ctypes.sizeof(wintypes.HMODULE)]:
        buf = ctypes.create_unicode_buffer(32768)
        if kernel.K32GetModuleFileNameExW(proc, handle, buf, len(buf)):
            paths.append(buf.value)
    return paths

print('PID:', os.getpid())
before = modules()
print('Before:', len(before))
assert not any(x.lower().endswith('winsqlite3.dll') for x in before)
library = ctypes.CDLL('winsqlite3.dll')
version = library.sqlite3_libversion
version.restype = ctypes.c_char_p
version.argtypes = []
print('SQLite:', version().decode())
after = modules()
print('After:', len(after))
for path in after:
    if path not in before:
        print('Added:', path)

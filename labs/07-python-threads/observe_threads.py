"""Состояния потоков и CPU за интервал без графического монитора."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

folder = Path(__file__).resolve().parent
def snapshot(number):
    command = (
        f'$p=Get-Process -Id {number}; '
        '[pscustomobject]@{PID=$p.Id;CPU=$p.CPU;'
        'Threads=@($p.Threads | Select-Object Id,ThreadState,'
        '@{n="CPU";e={$_.TotalProcessorTime.TotalSeconds}})} | ConvertTo-Json -Depth 5'
    )
    return json.loads(subprocess.check_output(['powershell','-NoProfile','-Command',command],text=True))

observations=[]
for executable in sys.argv[1:]:
    child = subprocess.Popen([executable, str(folder/'spin.py')], stdout=subprocess.PIPE, text=True)
    try:
        time.sleep(3)
        first = snapshot(child.pid)
        beginning = time.perf_counter()
        time.sleep(5)
        last = snapshot(child.pid)
        elapsed = time.perf_counter() - beginning
        observations.append(dict(executable=executable,logical=os.cpu_count(),first=first,last=last,elapsed=elapsed))
        child.wait(timeout=20)
    finally:
        if child.poll() is None:
            child.terminate()
            child.wait()
(folder/'evidence/spin.json').write_text(json.dumps(observations,indent=2))
print(json.dumps(observations,indent=2))

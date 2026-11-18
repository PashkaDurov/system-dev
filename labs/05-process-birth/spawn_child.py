import subprocess

completed = subprocess.run(["hostname"], capture_output=True, text=True)
print(completed.stdout.strip())
print("child exit code:", completed.returncode)

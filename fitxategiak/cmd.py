
import subprocess

try:
    f = input(">")
    result = subprocess.run(["powershell", "-Command",f], capture_output=True, text=True,timeout=2)
    print(result.stdout)
except subprocess.TimeoutExpired:
    print("finalize")

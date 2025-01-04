
import subprocess

result = subprocess.run(["powershell", "-Command", "cp"], capture_output=True, text=True)
print(len(result.stdout))
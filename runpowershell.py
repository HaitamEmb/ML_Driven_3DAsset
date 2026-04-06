import time
import subprocess
import re

def run_powershell_script(pred_curl):
    script_path = "C:/Users/Haitam/Desktop/haircardmain/mainHouScript.ps1"
    pred_curl = float(pred_curl)
    process = subprocess.Popen(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path, str(pred_curl)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    output, error = process.communicate()
    if output:
      print(f"PowerShell Script Output: {output}")
    if error:
      print(f"PowerShell Script Error: {error}")

def open_houdini_with_file(file_path):
    houdini_exe = "C:/Program Files/Side Effects Software/Houdini 19.5.303/bin/houdini.exe"  # Update to your Houdini version & path
    try:
        subprocess.Popen([houdini_exe, file_path], shell=True)
        print(f"Houdini launched with {file_path}")
    except Exception as e:
        print(f"Error launching Houdini: {e}")
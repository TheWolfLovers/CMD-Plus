import subprocess
import time
import os
mods = []
"""



try:
    with open(f"Addons\\{load}.pyext", "r") as file:
        code = file.read()
        exec(code)
except FileNotFoundError:
    print(f"Error: File '{load}.pyext' not found.")
    input()
except Exception as e:
    print("An error occurred:", e)
    input()
"""

rawFiles = os.listdir("Addons\\")
for i in range(len(rawFiles)):
    fileCheck = rawFiles[i]
    if fileCheck.endswith(".pyext"):
        mods.append(fileCheck)
        
for i in range(len(mods)):
    with open(r"Addons\\" + mods[i], "r") as file:
        code = file.read()
        exec(code)

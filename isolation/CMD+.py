# Basic ass code improved!!
# CMD+ Launcher 1.0

#---------[ Modules ]---------#
import os
import random
import sys
import time
import shutil
import plyer
import platform
import subprocess
from plyer import notification
import winsound
import tkinter
import playsound
import json
notif = notification
#-----------------------------#
#check 1
try:
    # access directory "bin"
    os.chdir("bin")
    try:
        subprocess.run(["python", "CMD+.py"], check=True)
    except subprocess.CalledProcessError as e:
        notif.notify(
            title="Error",
            message=f"Error executing CMD+: {e}",
            timeout=30
        )
    exit()
        
# Send a notif saying that it failed and output
# Saying what the error is (most likely that the
# directory doesn't exist
except OSError as e:
    notif.notify(
        title = "Error",
        message = f"Error from OS: {e}",
        timeout=8)
    exit()

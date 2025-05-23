import threading
import time
from blessed import Terminal
import vlc
import os

term = Terminal()
thr = threading.Thread

def killSwitch():
    with term.cbreak():
        while True:
            key = term.inkey(timeout=0.5)
            if key.name == "KEY_ESCAPE":
                print("program killed")
                os._exit(1)

exit = thr(target=killSwitch)
exit.start()

def Music():
    song = vlc.MediaPlayer("daichi.wav")
    song.play()
    
    with term.cbreak():
        while True:
            key = term.inkey(timeout=0.01)
            if key == "o":
                song.pause()

PlaySong = thr(target=Music)
PlaySong.start()

print("Program running")
timeD = 0
while True:
    time.sleep(1)
    timeD = timeD + 1
    print(timeD)


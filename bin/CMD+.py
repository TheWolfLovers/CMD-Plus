#imports
import sys
sys.path.append("lib")
sys.path.append("Mods/Lib")
import random
import platform
import os
import time
import platform
from plyer import email
from plyer import notification
from plyer import battery
#import winsound
import subprocess
import json
from blessed import Terminal
term = Terminal()
import threading
thr = threading.Thread
import vlc
########################################################
#important variables
modScripts = []
modFolders = []
rawModPacks = []
enabledModPacks = []
Batt = battery.status['percentage']
Charg = battery.status['isCharging']
ver = "Alpha 0.1.4 revamped"
Credentials = []
power = "ON" # Shits tying the startup with duct tape bro.
OriginalWorkingFolder = os.getcwd()
userName = ""
########################################################

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Settings
requireSignIn = True
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Old ass code from Alpha 0.1.5
def cls():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
def load():
    prin("[---")
    stutter = random.randint(1,3)
    time.sleep(stutter)
    prin("----")
    stutter = random.randint(1,3)
    time.sleep(stutter)
    prin("---")
    stutter = random.randint(1,3)
    time.sleep(stutter)
    prin("--\\")
    stutter = random.randint(1,3)
    time.sleep(stutter)
    print(" Done!!")
    
            
def prin(text):
    for char in text:
        print(char,end='',flush=True)
        time.sleep(0.05)

def shutdown(silent=False):
    if silent == False:
        print("System shutting down...")
        time.sleep(0.25)
        sys.exit()
    elif silent == True:
        time.sleep(0.5)
        sys.exit()

def update():
    print("updated! installing...")
        
    with open("CMD+.pydoc", "r") as source:
        content = source.read()
    with open("CMD+.BACKUP.py", "w") as backup:
        backup.write(content)
        print(f"CMD+ is backing up the current version {ver} please wait")
        load()
        print(f"CMD+ version {ver} has been backed up, updating...")
        load()
        
    with open("update.pldoc", "r") as file6:
        update = file6.read()
        with open("CMD+.py", "w") as f:
            f.write(update)
            shutdown()
        

def backup():
    with open("CMD+.py", "r") as source:
        content = source.read()
    with open("CMD+.BACKUP.py", "w") as backup:
        backup.write(content)
        print(f"CMD+ version {ver} backing up into CMD+.BACKUP.py... Please wait...")
        load()

def restore():
    #open CMD+.BACKUP.py in read mode
        #(file could be named anything, but in case of an emergency i made it a python so you can open and restore it :) )
        with open("CMD+.BACKUP.py", "r") as restore:
            #stores the code into a variable
            code = restore.read()
            #reads the file
            print("Backup file found... reading...")
            time.sleep(5)
            #opens restore cache
            with open("CMD+RestoreCache.pldoc", "w") as cache:
                #caches backup file
                cache.write(code)
                print("Backup file cached...")
                time.sleep(2)
                #reads cache
                with open("CMD+RestoreCache.", "r") as cacheR:
                    code2 = cacheR.read()
                    print("Reading cached backup...")
                    #opens original program as "subject" (i prefer "target")
                    with open("CMD+.py", "w") as subject:
                        print("Replacing program with backup....")
                        #starts writing the backup to the original code
                        time.sleep(5)
                        subject.write(code2)
                        time.sleep(3)
                        print("Done!")
                        shutdown()
            
def SignIn(userSel="none"):
    global userName
    tries = 4
    signedIn = False
    try:
        with open("account.pldoc", "r") as raw:
            loginDet = json.load(raw)

            if userSel == "none":
                usernamePass = input("Enter your username\n(/> ")
                passwordPass = input("Enter your password\n(/> ")
                for user in loginDet["users"]:
                    if user["username"] == usernamePass and user["password"] == passwordPass:
                        print("Signing in...")
                        time.sleep(1)
                        cls()
                        userName = user['username']
                        break
                    else:
                        print("Incorrect username or password. Terminating...")
                        shutdown(silent=True)
            else:
                print(f"Logging in as {userSel}...")
                passwordPass = input("Enter your password\n(/> ")
                for user in loginDet["users"]:
                    if user["username"] == userSel:
                        if user["password"] == passwordPass:
                            print("Signing in...")
                            time.sleep(1)
                            cls()
                            userName = user["username"]
                            
                                
                        else:
                            print("Incorrect username or password.")
                            return False
                    
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"users":[]}

        print("No accounts present, or account file corrupt\nStarting from scratch")
        newUsername = input("Enter new Username\n(/> ")
        newPassword = input("Enter new Password\n(/> ")
        data["users"].append({"username": newUsername, "password": newPassword})
        with open("account.pldoc", "w") as raw:
            json.dump(data, raw, indent=4)
            userName = newUsername
        
                            
            
def exit():
    shutdown()

        
def accConfig():

    with open("account.pldoc", "r") as file:
        data = json.load(file)
    def save():
        with open("account.pldoc", "w") as file:
            json.dump(data, file, indent=4)
    action = input("Right, you are now configuring your account\n\nChange password = 1\nChange username = 2\nAdd account = 3\nSwitch Accounts = 4\nDelete account = 5\n(/> ")

    if action == "1":
        newPassword = input("Enter new password")
        for user in data["users"]:
            if user["username"] == userName:
                user["password"] = newPassword
                save()
                print(f"Password for '{userName}' has been updated")
    #same as 1 but instead of password its the username
    elif action == "2":
        newUsername = input("Enter new username")
        for user in data["users"]:
            if user["username"] == userName:
                user["username"] = newUsername
                save()
                print(f"Password for '{userName}' has been updated to '{newUsername}'")
    #delete account

    elif action == "3":
        #add account logic
        newUsername = input("Who will this extra user be called?\n(/> ")
        newPassword = input("What will their password be?\n(/> ")
        data['users'].append({"username":newUsername, "password":newPassword})
        save()

    elif action == "4":
        # Switch accounts
        print("Who will will you sign in as?")
        choices = []
        for users in data["users"]:
            print(f'- {users["username"]}')
            choices.append(users["username"])
        select = input("{/> ")
        if select in choices:
            SignIn(select)
            print(f'''So {userName}, what are you going to do?''')
            
            
    elif action == "5":
        for user in data["users"]:
            if user["username"] == userName:
                passWord = user["password"]

                data["users"].remove({"username":userName, "password":passWord})
                save()
        if input("Account deleted\nDo you want to carry on using CMD+?\n(y/n)\n{/> ") == "y":
            print("Ok")
        else:
            print("Oh... hope to see you again soon!")
            time.sleep(3)
            shutdown()
    else:
        print("Sorry, incorrect action")
        time.sleep(2)

        
def logReader(): # Let's make everything json! Bookmark: JSONLOGS
    prin("Log Reader 2.0")
    print("\n\t[ Select a Log to read ]")
    try:
        FileList = []
        LogsList = []
        FileList = os.listdir(f"Users/{userName}/Files/Logs/")
        for i in range(len(FileList)):
            Files = FileList[i]
            if Files.endswith(".txt") or FileList.endswith(".pydoc"):
                LogsList.append(Files)

        for i in range(len(LogsList)):
            print("- " + LogsList[i])
        logno = input("Which log do you want to read?\n(defined by its log number)\n{/> ")
        try:
            with open(f"Users/{userName}/Files/Logs/Log{logno}.txt", "r") as log:
                lines = log.readlines()
                if len(lines) >= 3:
                    logno = lines[0].strip()
                    logtitle = lines[1].strip()
                    logdet = lines[3:]
                    print("reading Log...\n")
                    time.sleep(2)
                    prin(f"Log: {logno} \n")
                    prin(f"{logtitle}\n\n")
                    prin(logdet)
                    #read the logs you write :D
                    input("\n\nonce you\'ve done reading you can press enter to exit")
            #if file not found :/
        except FileNotFoundError:
            prin(f"\nThe Log {logno} you was looking for doesnt exist, check if it's the right number\n\n")
    except Exception as e:
        print(f"Oops... an error occured: {e}")
def logWriter():
    #write a log and call it whatever :D
    logno = input("What number is your Log?\n(/> ")
    logtitle = input("What's the title for this log?\n[/> ")
    logdet = ''
    print("Enter log description\n\ttype \':w\' to save and quit\n\n")
    while True:
        line = input(">")
        if line == ':w':
            break
        else:
            logdet += line + '\n'

    try:    
        with open(f"Users/{userName}/Files/Logs/Log{logno}.txt", "w") as log:
            log.writelines(logno + '\n' + logtitle + '\n\n' + logdet)
            print(f"\n\nWriting Log {logno} titled {logtitle}...")
            load()
    except FileNotFoundError:
        os.makedirs(f"Users/{userName}/Files/Logs/")
        with open(f"Users/{userName}/Files/Logs/Log{logno}.txt", "w") as log:
            log.writelines(logno + '\n' + logtitle + '\n\n' + logdet)
            print(f"\n\nWriting Log {logno} titled {logtitle}...")
            load()

def write():
    pass

def help():
    print("All useable commands:\n")
    for i in commands.keys():
        print(f" - {i}")
    print("\n")
    input("Enter to exit")
    print("\n")




def say(arg):
    print(arg)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Generated with chatgpt
def CMD():
    current_dir = os.getcwd()
    
    while True:
        command = input(f"{current_dir}> ").strip()
        
        if command.lower() in {"exit", "quit"}:
            break
        
        if command.startswith("cd "):
            try:
                new_dir = command[3:].strip()
                os.chdir(new_dir)
                current_dir = os.getcwd()
            except FileNotFoundError:
                print(f"The directory {new_dir} does not exist.")
            except Exception as e:
                print(f"Error changing directory: {e}")
        else:
            try:
                result = subprocess.run(command, shell=True, cwd=current_dir, capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            except Exception as e:
                print(f"Error executing command: {e}")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
acceptedModFolders = [
    "Music",
    "Scripts",
    "Text",
    "Text/System",
    "Text/Documents",
    "Sounds"]
rawFolders = []
rawFiles = []
def loadFolders():
    global rawModPacks
    global enabledModPacks
    rawModPacks.clear()
    enabledModPacks.clear()
    rawFolders = []
    
    # Load raw files and folders
    rawFilesNFolders = os.listdir("Mods/")

    # Separate out folders from files
    for item in rawFilesNFolders:
        if os.path.isdir(os.path.join("Mods", item)):
            rawFolders.append(item)
    
    # Filter accepted mods folders and handle meta.json
    for f in rawFolders:
        if f in acceptedModFolders:
            modFolders.append(f)
        elif f not in acceptedModFolders:
            metadataFile = os.path.join("Mods", f, "meta.json")
            try:
                with open(metadataFile, 'r') as rawdata:
                    metadata = json.load(rawdata)
                    if "name" in metadata and "description" in metadata and "toggled" in metadata:
                        rawModPacks.append(f)
                        if metadata["toggled"]:
                            enabledModPacks.append(f)
            except Exception:
                pass

    print(f"Loaded {len(rawModPacks)} mod {'pack' if len(rawModPacks) == 1 else 'packs'} | {len(enabledModPacks)} mod {'pack' if len(enabledModPacks) == 1 else 'packs'} enabled")




def loadScripts():
    # Load base scripts if exists
    if os.path.isdir(os.path.join("Mods", "Scripts")):
        baseScripts = []
        rawFiles = os.listdir("Mods/Scripts")
        for fileCheck in rawFiles:
            if fileCheck.endswith(".pyext"):
                baseScripts.append(fileCheck)
        for script in baseScripts:
            with open(f"Mods/Scripts/{script}", 'r') as source:
                code = source.read()
                exec(code)

    modpackScripts = []
    for mod in enabledModPacks:
        modpack = f"Mods/{mod}/Scripts"
        if os.path.isdir(modpack):
            modpackScripts = []  # Clear previous scripts
            rawFiles = os.listdir(modpack)
            for fileCheck in rawFiles:
                if fileCheck.endswith(".pyext"):
                    modpackScripts.append(fileCheck)
            for script in modpackScripts:
                with open(f"{modpack}/{script}", 'r') as source:
                    code = source.read()
                    exec(code)

    # Merge base and modpack scripts
    allScripts = baseScripts + modpackScripts
    print(f"Loaded {len(allScripts)} {'script' if len(allScripts) == 1 else 'scripts'}")
    global modScripts
    modScripts = allScripts


def reloadMods():
    loadFolders()
    loadScripts()

def openCMDPlusDir():
    os.startfile(OriginalWorkingFolder)


def Settings():
    def modpacks():
        

                
        print("All modpacks installed:\n")
        for i in rawModPacks:
            with open(f"Mods/{i}/meta.json", "r") as raw:
                meta = json.load(raw)
            print(f" - {i} - {meta['name']} | {meta['description']}")
        print("\nAll enabled modpacks:\n")
        for i in enabledModPacks:
            with open(f"Mods/{i}/meta.json", "r") as raw:
                meta = json.load(raw)
            print(f" - {i} - {meta['name']} | {meta['description']}")
        
        print("\nWhich one do you want to select?")
        select = input("{/> ")
        if select in rawModPacks:
            print("Do you want to enable it?")
            toggle = input("{ Y/N /> ").lower()
            if toggle == "y":
                toggle = True
            elif toggle == "n":
                toggle = False
            with open(f"Mods/{select}/meta.json", "r") as raw:
                meta = json.load(raw)
                meta['toggled'] = toggle
                with open(f"Mods/{select}/meta.json", "w") as rawtowrite:
                    json.dump(meta, rawtowrite, indent=4)
        reloadMods()
                
                    
    settings = {
        "Modpacks": modpacks
        }
    print("Which setting do you want to edit?")
    for i in settings.keys():
        print(f" - {i}")
    selector = input("{/> ")
    if selector in settings:
        settings[selector]()
    
    
    
    

with open("Settings.txt", "r") as settings:
    settingsLoad = settings.read()
    exec(settingsLoad)











#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#check if account already exists, if not, create one, if yes, then sign in
#i dont normally do comments but here i am!! - 18/03/2024
#   I don't need the original algorithim to check "CreatedAccount.pldoc" because I
# Now have a friggin' JSON FILE WOO- 31/01/2025
SignIn()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Functions (Commands)
def PlayMusic(song):
    path = os.path.abspath(f"./Mods/Music/{song}")
    player = vlc.MediaPlayer(f"file://{path}")
    player.play()

def MusicMenu(arg=""):
    if arg == "":
        songList = []
        if os.path.isdir("Mods/Music"):
            files = os.listdir("Mods/Music")
            for i in range(len(files)):
                fileCheck = files[i]
                if fileCheck.endswith(".wav") or fileCheck.endswith(".mp3"):
                    songList.append(fileCheck)
            print("Song List\n(Found in Mods/Music)")
            for i in range(len(songList)):
                displaySong = songList[i]
                print(i + 1, "-", displaySong)
            print("\nInput which song you want to play")
            temp = int(input("{/> "))
            songChosen = songList[temp - 1]
            print("Now playing: ", songChosen)
            MusicThread = thr(target=PlayMusic, args=(songChosen,))
            MusicThread.start()
            
            

































#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
commands = {
    "[ All the help commands ]": "",
    "/help": help,
    "help": help,
    "/list": help,
    "list": help,
    "[ Main commands ]": "",
    "/write": write,
    "/accountconfig": accConfig,
    "/log": logReader,
    "/wlog": logWriter,
    ">update": update,
    ">restore": restore,
    ">backup": backup,
    "/say": say,
    ">exit": exit,
    "/cmd": CMD,
    "/dir": openCMDPlusDir,
    "/reload": reloadMods,
    "/settings": Settings,
    "settings": Settings,
    "/music": MusicMenu,
    "[ Mods: ]": ""
    }

loadFolders()
loadScripts()




print("        Welcome back ^^")
# Main
print(f'''So {userName}, what are you going to do?''')
#while the power = ON keep asking for an input "action"
while power == "ON":
    cmdIn = input(f"[ {userName} /> ")
    if cmdIn == "":
        pass
    else:
        parts = cmdIn.split(maxsplit=1)
        cmdExe = parts[0]
        arg = parts[1:] if len(parts) > 1 else ''

        if cmdExe in commands:
            try:
                commands[cmdExe](*arg)
            except Exception as e:
                print(e)
        else:
            print(f"\n{cmdExe} is not a valid command\nplease try again\n")



# end of program
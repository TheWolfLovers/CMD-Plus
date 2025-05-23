import os

rawFilesNFolders = []
rawFolders = []
rawFiles = []

modFolders = []
'''def modLoader():
    
    rawFiles = os.listdir("Mods\\")
    for i in range(len(rawFiles)):
        fileCheck = rawFiles[i]
        if fileCheck.endswith(".pyext"):
            mods.append(fileCheck)
            
    for i in range(len(mods)):
        with open(r"Mods\\" + mods[i], "r") as file:
            code = file.read()
            exec(code)
    return code'''


acceptedModFolders = {
    "Music",
    "Scripts",
    "Text",
    "Text\\System",
    "Text\\Documents",
    "Sounds"}

def loadFolders():
    # loads raw files and folders
    rawFilesNFolders = os.listdir("Mods\\")

    # seperates out folders from files
    for item in rawFilesNFolders:
        if os.path.isdir(os.path.join("Mods", item)):
            rawFolders.append(item)
    # if its an accepted mods folder. add it.
    for f in rawFolders:
        if f in acceptedModFolders:
            modFolders.append(f)


def loadScripts():
    if os.path.isdir(os.path.join("Mods", "Scripts")):
        rawFiles = os.listdir("Mods\\Scripts")
        for i in range(len(rawFiles)):
            fileCheck = rawFiles[i]
            if fileCheck.endswith(".pyext"):
                modScripts.append(fileCheck)


modLoader()
print("end")

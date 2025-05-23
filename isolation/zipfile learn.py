import zipfile
import os
import json
zipl = zipfile.ZipFile

from blessed import Terminal

term = Terminal()

def multin(inp = ''):
    print("\n-=[ Log Editor ]=-\nEntering text editor. Press ESC or Ctrl+S to finish.")
    input("Press Enter to start...")

    lines = inp.split('\n') if inp != '' else ['']
    x, y = 0, 0
    scroll = 0
    height = term.height - 2  # one line for title, one extra for buffer

    with term.fullscreen(), term.cbreak():
        while True:
            # Draw title bar (white background, black text)
            title_text = " CMD+ Log Writer (Alpha) - CTRL+S to save (or ESC) "
            title = title_text.center(term.width)
            print(term.home + term.on_white + term.black + title + term.normal)


            # Clamp x and scroll
            x = min(x, len(lines[y]))
            if y < scroll:
                scroll = y
            elif y >= scroll + height:
                scroll = y - height + 1

            # Draw visible lines below title bar (start from row 1)
            print(term.move(1, 0) + term.clear_eos, end='')
            for i in range(scroll, min(scroll + height, len(lines))):
                print(term.move(i - scroll + 1, 0) + lines[i])

            # Move cursor (offset by 1 row for title)
            print(term.move(y - scroll + 1, x), end='', flush=True)

            key = term.inkey()

            if not key:
                continue

            if key.name == 'KEY_ESCAPE' or key == '\x13':  # ESC or Ctrl+S
                break
            elif key.name == 'KEY_ENTER':
                lines.insert(y + 1, lines[y][x:])
                lines[y] = lines[y][:x]
                y += 1
                x = 0
            elif key.name == 'KEY_BACKSPACE':
                if x > 0:
                    lines[y] = lines[y][:x - 1] + lines[y][x:]
                    x -= 1
                elif y > 0:
                    x = len(lines[y - 1])
                    lines[y - 1] += lines[y]
                    del lines[y]
                    y -= 1
            elif key.name == 'KEY_UP':
                if y > 0:
                    y -= 1
            elif key.name == 'KEY_DOWN':
                if y < len(lines) - 1:
                    y += 1
            elif key.name == 'KEY_LEFT':
                if x > 0:
                    x -= 1
                elif y > 0:
                    y -= 1
                    x = len(lines[y])
            elif key.name == 'KEY_RIGHT':
                if x < len(lines[y]):
                    x += 1
                elif y + 1 < len(lines):
                    y += 1
                    x = 0
            elif key.is_sequence is False and key:
                lines[y] = lines[y][:x] + key + lines[y][x:]
                x += 1

        print(term.normal, end='')
    return '\n'.join(lines)

userName = "iso"

response_type = {
    "no": ["no","nope", "negative", "-", "nah"],
    "yes": ["yes","yeah","yep","positive","+"]
}

def logWriter():
    #write a log and call it whatever :D
    logno = input("What number is your Log?\n(/> ")
    logtitle = input("What's the title for this log?\n[/> ")
    logdet = multin()

    print("#- = -#\n\n\nYou wrote:\n")
    print(logdet)
    confirm = input("\n#-End of File-#\n\nAre you sure?\n{/>")
    while confirm in response_type["no"]:
        logdet = multin(logdet)
        print("#- = -#\n\n\nYou wrote:\n")
        print(logdet)
        confirm = input("\n#-End of File-#\n\nAre you sure?\n{/>")

    try:                
        with zipl(f"Users/{userName}/Files/Logs/Log" + logno + ".pllog", "w") as logf:
            metadata = json.dumps({'logNum': logno, 'logTitle': logtitle})
            logf.writestr("metadata.json", metadata)
            logf.writestr("text.txt", logdet)
    except FileNotFoundError:
        os.makedirs(f"Users/{userName}/Files/Logs/")
            
        with zipl(f"Users/{userName}/Files/Logs/Log" + logno + ".pllog", "w") as logf:
            metadata = json.dumps({'logNum': logno, 'logTitle': logtitle})
            logf.writestr("metadata.json", metadata)
            logf.writestr("text.txt", logdet)







def logReader(): # Let's make everything json! Bookmark: JSONLOGS
    print("Log Reader 2.0")
    print("\n\t[ Select a Log to read ]")
    try:
        FileList = []
        LogsList = []
        FileList = os.listdir(f"Users/{userName}/Files/Logs/")
        for i in range(len(FileList)):
            Files = FileList[i]
            if Files.endswith(".pllog"):
                LogsList.append(Files)

        for i in range(len(LogsList)):
            print("- " + LogsList[i])
        logno = input("Which log do you want to read?\n(defined by its log number)\n{/> ")
        try:
            with zipl(f"Users/{userName}/Files/Logs/Log{logno}.pllog", "r") as logzip:
                rawdata = logzip.read("metadata.json").decode()
                textcontent = logzip.read("text.txt").decode()
                metadata = json.loads(rawdata)

                print(f"Log: {metadata['logNum']}\n")
                print(metadata['logTitle'] + "\n\n")
                print(textcontent)
        except FileNotFoundError:
            print(f"\nThe Log {logno} you was looking for doesnt exist, check if it's the right number\n\n")
    except Exception as e:
        print(f"Oops... an error occured: {e}")

logReader()
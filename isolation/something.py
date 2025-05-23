from blessed import Terminal

term = Terminal()

def multiline_input():
    print("Entering text editor. Press ESC or Ctrl+S to finish.")
    input("Press Enter to start...")

    lines = ['']
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

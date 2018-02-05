import curses
import math
import pprint

def add_text(win, text, box_width=80, pad=1):
    text_width = box_width - 2 * pad

    printer = pprint.PrettyPrinter(stream=None, indent=0, width=text_width, depth=None,
        compact=False)

    lines = printer.pformat(text)
    lines = lines.split("\n")
    for idx, line in enumerate(lines):
        win.addstr(idx+2, 2, line[2:-2])

# Read the file
path_to_store = "/home/matthias/Pictures/PicOfDay/"

with open(path_to_store + "description.txt") as desc:
    lines = desc.readlines()

title = lines[0]
text = lines[1].strip()


# Inint
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
stdscr.refresh()

# Make the box
box_width = 80
n_lines = int(math.ceil(len(text)/box_width))
box_height = n_lines + 5

win = curses.newwin(box_height, box_width, 0, 1)
win.box()
win.addstr(1, 2, lines[0].strip(), curses.A_BOLD)
add_text(win, text)
win.refresh()

# Close
c = stdscr.getch()
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
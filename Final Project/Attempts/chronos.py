import time
import sys
import json
import os
from datetime import datetime

# Keyboard helpers — Windows uses msvcrt; macOS uses termios/tty.
IS_WINDOWS = sys.platform == "win32"
if IS_WINDOWS:
    import msvcrt
else:
    import fcntl
    import struct
    import termios
    import tty

def key_pressed():
    if IS_WINDOWS:
        return msvcrt.kbhit()  # Windows API name
    if not sys.stdin.isatty():
        return False
    pending = fcntl.ioctl(sys.stdin.fileno(), termios.FIONREAD, struct.pack("I", 0))
    return struct.unpack("I", pending)[0] > 0

def save_input_mode():
    if IS_WINDOWS or not sys.stdin.isatty():
        return None
    return termios.tcgetattr(sys.stdin.fileno())

def restore_input_mode(saved_settings):
    if saved_settings is not None:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, saved_settings)

def enable_key_mode():
    if not IS_WINDOWS and sys.stdin.isatty():
        tty.setcbreak(sys.stdin.fileno())

from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.align import Align
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.text import Text 
from plyer import notification 

# --- 1. SETUP ---
console = Console()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "tasks.json")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.clear()

# --- 2. DATA HANDLERS ---
def load_tasks():
    if not os.path.exists(DATA_FILE): return []
    try:
        with open(DATA_FILE, "r") as f: return json.load(f)
    except: return [] # If file is corrupted, return an empty list

def save_tasks(task_list):
    with open(DATA_FILE, "w") as f: json.dump(task_list, f, indent=4)

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%m/%d/%y")
    except: return date_str

# --- 3. RENDER LOGIC ---
def render_tasks(task_list):
    if not task_list:
        return Align.center("\n[italic grey42]No current tasks[/]\n[grey30]Press [[a]] to add one[/]", vertical="middle")
    task_list.sort(key=lambda x: x['due'])
    table = Table(box=None, show_header=True, expand=True, padding=(0, 1))
    table.add_column("#", style="dim", width=3)
    table.add_column("Task", style="white")
    table.add_column("Due", justify="right", style="cyan")

    for index, t in enumerate(task_list):
        display_date = format_date(t['due'])
        table.add_row(str(index + 1), f"• {t['name']}", display_date)
    return table

def render_timer(seconds):
    mins, secs = divmod(int(seconds), 60)
    return Align.center(f"\n[bold white]{mins:02d}:{secs:02d}[/]\n", vertical="middle")

def make_dashboard(tasks, remaining_seconds):
    layout = Layout()
    layout.split_column(Layout(name="main", ratio=1), Layout(name="footer", size=3))
    width = console.width
    if width < 60:
        layout["main"].split_column(Layout(name="timer_box", size=5), Layout(name="tasks_box", ratio=1))
    else:
        layout["main"].split_row(Layout(name="tasks_box", ratio=2), Layout(name="timer_box", ratio=1))

    layout["tasks_box"].update(Panel(render_tasks(tasks), title="Task List", border_style="blue"))
    layout["timer_box"].update(Panel(render_timer(remaining_seconds), title="Timer", border_style="blue"))

    f_menu = Text()
    f_menu.append("[a]", style="bold cyan"); f_menu.append(" - add | ")
    f_menu.append("[c]", style="bold cyan"); f_menu.append(" - complete | ")
    f_menu.append("[p]", style="bold cyan"); f_menu.append(" - pause | ")
    f_menu.append("[q]", style="bold cyan"); f_menu.append(" - quit")
    layout["footer"].update(Panel(Align.center(f_menu), border_style="white"))
    return layout

def show_dashboard(tasks, remaining_seconds):
    clear_screen()
    console.print(make_dashboard(tasks, remaining_seconds))

def wait_for_key():
    if IS_WINDOWS:
        while not key_pressed():
            time.sleep(0.05)
        return msvcrt.getch().decode("utf-8").lower()
    return sys.stdin.read(1).lower()

def add_task(tasks, terminal_settings):
    restore_input_mode(terminal_settings)
    name = Prompt.ask("\n[yellow]Task Name[/]")
    due_input = Prompt.ask("[yellow]Due (MM/DD/YY)[/]", default=datetime.now().strftime("%m/%d/%y"))
    try:
        date_obj = datetime.strptime(due_input, "%m/%d/%y")
        store_date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        store_date = datetime.now().strftime("%Y-%m-%d")
    tasks.append({"name": name, "due": store_date})
    save_tasks(tasks)
    enable_key_mode()

def complete_task(tasks, terminal_settings):
    restore_input_mode(terminal_settings)
    console.print("\n[bold cyan]Select task to complete (0 to Go Back):[/]")
    tasks.sort(key=lambda x: x['due'])
    for i, t in enumerate(tasks):
        console.print(f" [bold]{i+1}[/] - {t['name']} ({format_date(t['due'])})")
    choice = IntPrompt.ask("\n[green]Enter number[/]", default=0)
    if choice != 0 and 1 <= choice <= len(tasks):
        tasks.pop(choice - 1)
        save_tasks(tasks)
    time.sleep(0.5)
    enable_key_mode()

def start_timer(tasks, remaining_seconds):
    is_running = True
    last_tick_time = None
    layout = make_dashboard(tasks, remaining_seconds)

    with Live(layout, refresh_per_second=4, transient=True) as live:
        while is_running:
            now = datetime.now()
            if last_tick_time:
                elapsed = (now - last_tick_time).total_seconds()
                remaining_seconds = max(0, remaining_seconds - elapsed)
            last_tick_time = now

            if remaining_seconds <= 0:
                is_running = False
                notification.notify(title="Time's Up!", message="Session complete!", timeout=5)
                break

            layout["timer_box"].update(Panel(render_timer(remaining_seconds), title="Timer", border_style="blue"))

            if key_pressed():
                key = wait_for_key()
                if key == 'p':
                    is_running = False
                elif key == 'q':
                    sys.exit(0)
            time.sleep(0.05)

    return remaining_seconds

# --- 4. MAIN PROGRAM ---
def main():
    if not sys.stdin.isatty():
        console.print("[red]Run this program in a terminal (not the Run button).[/]")
        sys.exit(1)

    tasks = load_tasks()
    remaining_seconds = 25 * 60
    terminal_settings = save_input_mode()
    enable_key_mode()

    try:
        while True:
            show_dashboard(tasks, remaining_seconds)
            key = wait_for_key()

            if key == 'a':
                add_task(tasks, terminal_settings)
            elif key == 'c' and tasks:
                complete_task(tasks, terminal_settings)
            elif key == 'p':
                remaining_seconds = start_timer(tasks, remaining_seconds)
            elif key == 'q':
                break
    finally:
        restore_input_mode(terminal_settings)
        clear_screen()


if __name__ == "__main__":
    main()
# ==============================================================================
# DOCUMENTATION & STUDY RESOURCES
# ==============================================================================
"""
FUNCTION REFERENCE:
1. clear_screen(): 
   - Purpose: Aggressively wipes the terminal screen and scrollback buffer.
   - Implementation: Uses 'os.system' to call the OS-level 'cls' (Windows) or 'clear' (Unix) 
     command, followed by Rich's internal console.clear().

2. load_tasks() / save_tasks():
   - Purpose: Handles persistent storage for your tasks.
   - Implementation: Uses the 'json' library to read/write a list of dictionaries to 'tasks.json'.
     'load_tasks' includes error handling to prevent crashes if the file is missing or corrupted.

3. format_date(date_str):
   - Purpose: Converts internal ISO dates (YYYY-MM-DD) to user-friendly format (MM/DD/YY).
   - Implementation: Utilizes 'datetime.strptime' for parsing and 'strftime' for re-formatting.

4. render_tasks(task_list):
   - Purpose: Generates the Rich Table object for the main dashboard view.
   - Implementation: Sorts the list by the 'due' key so tasks stay in chronological order.

5. render_timer(seconds):
   - Purpose: Converts the countdown float into a formatted MM:SS string.
   - Implementation: Uses 'divmod' to split total seconds into minutes and seconds.

6. make_dashboard(tasks, remaining_seconds):
   - Purpose: Provides an adaptive/responsive UI for different terminal sizes.
   - Implementation: Monitors 'console.width' and toggles the layout between 'split_row' 
     (landscape) and 'split_column' (portrait).

--------------------------------------------------------------------------------
STUDY LINKS & RESOURCES:

UI & LAYOUT (Rich Library):
- Documentation: https://rich.readthedocs.io/en/latest/introduction.html
- Specific Study: Explore the 'Live Display' and 'Layout' sections.

DATE & TIME HANDLING (Datetime Library):
- Formatting Cheat Sheet: https://strftime.org/
- Tutorial: https://realpython.com/python-datetime/

SYSTEM INTERACTION (Msvcrt & Plyer):
- Keyboard Input (msvcrt): https://docs.python.org/3/library/msvcrt.html
- Notifications (Plyer): https://github.com/kivy/plyer

DATA PERSISTENCE (JSON):
- Python JSON Guide: https://www.w3schools.com/python/python_json.asp
"""
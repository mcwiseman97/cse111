import time
import msvcrt
import json
import os
from datetime import datetime

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

def nuclear_clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.clear()

# --- 2. DATA HANDLERS ---
def load_data():
    if not os.path.exists(DATA_FILE): return []
    try:
        with open(DATA_FILE, "r") as f: return json.load(f)
    except: return []

def save_data(task_list):
    with open(DATA_FILE, "w") as f: json.dump(task_list, f, indent=4)

def format_date_for_display(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%m/%d/%y")
    except: return date_str

# --- 3. RENDER LOGIC ---
def get_task_render(task_list):
    if not task_list:
        return Align.center("\n[italic grey42]No current tasks[/]\n[grey30]Press [[a]] to add one[/]", vertical="middle")
    task_list.sort(key=lambda x: x['due'])
    table = Table(box=None, show_header=True, expand=True, padding=(0, 1))
    table.add_column("#", style="dim", width=3)
    table.add_column("Task", style="white")
    table.add_column("Due", justify="right", style="cyan")

    for index, t in enumerate(task_list):
        display_date = format_date_for_display(t['due'])
        table.add_row(str(index + 1), f"• {t['name']}", display_date)
    return table

def get_timer_render(seconds):
    mins, secs = divmod(int(seconds), 60)
    return Align.center(f"\n[bold white]{mins:02d}:{secs:02d}[/]\n", vertical="middle")

def update_layout_structure(layout):
    width = console.width
    layout["main"].split()
    if width < 60:
        layout["main"].split_column(Layout(name="timer_box", size=5), Layout(name="tasks_box", ratio=1))
    else:
        layout["main"].split_row(Layout(name="tasks_box", ratio=2), Layout(name="timer_box", ratio=1))

# --- 4. MAIN PROGRAM ---
tasks = load_data()
is_running = False
remaining_seconds = 25 * 60
last_tick_time = None

layout = Layout()
layout.split_column(Layout(name="main", ratio=1), Layout(name="footer", size=3))

nuclear_clear()

with Live(layout, refresh_per_second=10, transient=True) as live:
    while True:
        update_layout_structure(layout)

        if is_running:
            now = datetime.now()
            if last_tick_time:
                elapsed = (now - last_tick_time).total_seconds()
                remaining_seconds = max(0, remaining_seconds - elapsed)
            last_tick_time = now
            if remaining_seconds <= 0:
                is_running = False
                notification.notify(title="Time's Up!", message="Session complete!", timeout=5)
        else:
            last_tick_time = None

        layout["tasks_box"].update(Panel(get_task_render(tasks), title="Task List", border_style="blue"))
        layout["timer_box"].update(Panel(get_timer_render(remaining_seconds), title="Timer", border_style="blue"))
        
        f_menu = Text()
        f_menu.append("[a]", style="bold cyan"); f_menu.append(" - add | ")
        f_menu.append("[c]", style="bold cyan"); f_menu.append(" - complete | ")
        f_menu.append("[p]", style="bold cyan"); f_menu.append(" - pause | ")
        f_menu.append("[q]", style="bold cyan"); f_menu.append(" - quit")
        layout["footer"].update(Panel(Align.center(f_menu), border_style="white"))

        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'a':
                live.stop()
                name = Prompt.ask("\n[yellow]Task Name[/]")
                due_input = Prompt.ask("[yellow]Due (MM/DD/YY)[/]", default=datetime.now().strftime("%m/%d/%y"))
                try:
                    date_obj = datetime.strptime(due_input, "%m/%d/%y")
                    store_date = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    store_date = datetime.now().strftime("%Y-%m-%d")
                tasks.append({"name": name, "due": store_date})
                save_data(tasks)
                nuclear_clear(); live.start()

            elif key == 'c' and tasks:
                live.stop()
                console.print("\n[bold cyan]Select task to complete (0 to Go Back):[/]")
                tasks.sort(key=lambda x: x['due'])
                for i, t in enumerate(tasks):
                    console.print(f" [bold]{i+1}[/] - {t['name']} ({format_date_for_display(t['due'])})")
                choice = IntPrompt.ask("\n[green]Enter number[/]", default=0)
                if choice != 0 and 1 <= choice <= len(tasks):
                    tasks.pop(choice - 1)
                    save_data(tasks)
                time.sleep(0.8)
                nuclear_clear(); live.start()

            elif key == 'p':
                is_running = not is_running
            elif key == 'q':
                break
        time.sleep(0.05)

# ==============================================================================
# DOCUMENTATION & STUDY RESOURCES
# ==============================================================================
"""
FUNCTION REFERENCE:
1. nuclear_clear(): 
   - Purpose: Aggressively wipes the terminal screen and scrollback buffer.
   - Implementation: Uses 'os.system' to call the OS-level 'cls' (Windows) or 'clear' (Unix) 
     command, followed by Rich's internal console.clear().

2. load_data() / save_data():
   - Purpose: Handles persistent storage for your tasks.
   - Implementation: Uses the 'json' library to read/write a list of dictionaries to 'tasks.json'.
     'load_data' includes error handling to prevent crashes if the file is missing or corrupted.

3. format_date_for_display(date_str):
   - Purpose: Converts internal ISO dates (YYYY-MM-DD) to user-friendly format (MM/DD/YY).
   - Implementation: Utilizes 'datetime.strptime' for parsing and 'strftime' for re-formatting.

4. get_task_render(task_list):
   - Purpose: Generates the Rich Table object for the main dashboard view.
   - Implementation: Sorts the list by the 'due' key so tasks stay in chronological order.

5. get_timer_render(seconds):
   - Purpose: Converts the countdown float into a formatted MM:SS string.
   - Implementation: Uses 'divmod' to split total seconds into minutes and seconds.

6. update_layout_structure(layout):
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
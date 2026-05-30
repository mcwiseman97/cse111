import os # Helps with file directory lookup and modifcations
import time 
import json # Ability to work with, read write json files (My storage option)
import sys # Helps with identifying the operating system ()

from datetime import datetime

# Rich Packages
from rich.layout import Layout # Organize Boxes
from rich.color import Color # Change terminal text colors
from rich.align import Align # Align text in a box
from rich.table import Table # Will help make the task grid for taks | date seperation
from rich.style import Style # Bg color, text color, text decorations
from rich.panel import Panel # Makes the border box's
from rich.live import Live # Allows for the terminal boxes to be dynamic
from rich.console import Console # Allows for clearing the console


from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.align import Align
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.text import Text 

# Main contains all the core visual elements of the program

def main():
    layout = Layout()

    layout.split_column(Layout(name="main", ratio=1), Layout(name="footer", size=3))
    layout["tasks_box"].update(Panel(get_task_render(tasks), title="Task List", border_style="blue"))
    layout["timer_box"].update(Panel(get_timer_render(remaining_seconds), title="Timer", border_style="blue"))

if __name__ == "__main__":
    main()
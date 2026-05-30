import time
import sys
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

# Global variables
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "tasks.json")


# Clearing the console
console = Console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.clear()

# Data related functions

# If file does not exist, create it
# If file exists, load it
def load_file():
    if not os.path.exists(DATA_FILE): return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except: return [] # If file is corrupted, return an empty list

# Write data to file
def write_file(tasks):
    with open(DATA_FILE, "w") as f: json.dump(tasks, f, indent=4)

# Date configuration
def format_date(date_str):
    pass
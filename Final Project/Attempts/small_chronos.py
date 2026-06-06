import json
import os
import time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "small_tasks.json")
DEFAULT_TIMER_SECONDS = 25 * 60


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(task_list):
    with open(DATA_FILE, "w") as file:
        json.dump(task_list, file, indent=4)


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%m/%d/%y")
    except ValueError:
        return date_str


def parse_due_date(due_input):
    try:
        date_obj = datetime.strptime(due_input, "%m/%d/%y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return datetime.now().strftime("%Y-%m-%d")


def format_timer(seconds):
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def get_task_lines(tasks):
    if not tasks:
        return ["No tasks yet."]

    sorted_tasks = sorted(tasks, key=lambda task: task["due"])
    lines = []
    for index, task in enumerate(sorted_tasks, start=1):
        due = format_date(task["due"])
        lines.append(f"{index}. {task['name']}  Due: {due}")
    return lines


def show_tasks(tasks):
    for line in get_task_lines(tasks):
        print(line)


def show_menu():
    print("1. Add task")
    print("2. Complete task")
    print("3. Start timer")
    print("4. Quit")


def add_task(tasks):
    name = input("Task name: ").strip()
    if not name:
        print("Task name cannot be empty.")
        return

    due_input = input("Due (MM/DD/YY): ").strip()
    if not due_input:
        due_input = datetime.now().strftime("%m/%d/%y")

    tasks.append({"name": name, "due": parse_due_date(due_input)})
    save_tasks(tasks)
    print("Task added.")


def complete_task(tasks):
    if not tasks:
        print("No tasks to complete.")
        return

    sorted_tasks = sorted(tasks, key=lambda task: task["due"])
    for index, task in enumerate(sorted_tasks, start=1):
        print(f"{index}. {task['name']} ({format_date(task['due'])})")

    choice_text = input("Task number to complete (0 to cancel): ").strip()
    try:
        choice = int(choice_text)
    except ValueError:
        print("Please enter a number.")
        return

    if choice == 0:
        return

    if 1 <= choice <= len(sorted_tasks):
        removed = sorted_tasks.pop(choice - 1)
        tasks[:] = sorted_tasks
        save_tasks(tasks)
        print(f"Completed: {removed['name']}")
    else:
        print("Invalid task number.")


def start_timer(seconds):
    while seconds > 0:
        print(f"Timer: {format_timer(seconds)}", end="\r", flush=True)
        time.sleep(1)
        seconds -= 1

    print("\nTime's up!")
    return 0


def main():
    tasks = load_tasks()
    remaining_seconds = DEFAULT_TIMER_SECONDS

    while True:
        clear_screen()
        print("CHRONOS")
        print(f"Timer: {format_timer(remaining_seconds)}")
        print()
        show_tasks(tasks)
        print()
        show_menu()

        choice = input("Choice: ").strip()

        if choice == "1":
            add_task(tasks)
            input("Press Enter to continue...")
        elif choice == "2":
            complete_task(tasks)
            input("Press Enter to continue...")
        elif choice == "3":
            remaining_seconds = start_timer(remaining_seconds)
        elif choice == "4":
            clear_screen()
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()

"""
Rich CLI Interactive Guide
==========================
Run:  python rich_cli_guide.py

A hands-on tour of Rich — the library that makes terminal apps look polished.
Each menu option shows a live demo plus notes you can reuse in your own projects.
"""

from __future__ import annotations

import time

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.style import Style
from rich.table import Table
from rich.text import Text

console = Console()

# ---------------------------------------------------------------------------
# Study resources (also shown inside the program)
# ---------------------------------------------------------------------------
RESOURCES = """
## Rich Documentation & Links

| Topic | URL |
|-------|-----|
| **Main docs** | https://rich.readthedocs.io/en/latest/introduction.html |
| **Console** | https://rich.readthedocs.io/en/latest/console.html |
| **Panel** | https://rich.readthedocs.io/en/latest/panel.html |
| **Table** | https://rich.readthedocs.io/en/latest/tables.html |
| **Style & markup** | https://rich.readthedocs.io/en/latest/style.html |
| **Layout** | https://rich.readthedocs.io/en/latest/layout.html |
| **Live display** | https://rich.readthedocs.io/en/latest/live.html |
| **Prompts** | https://rich.readthedocs.io/en/latest/prompt.html |
| **Text object** | https://rich.readthedocs.io/en/latest/text.html |

**Install:** `pip install rich`

**Minimal CLI skeleton:**
```python
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    console.print(Panel("Hello from Rich!", title="My App"))

if __name__ == "__main__":
    main()
```
"""

MENU = """
[bold cyan]Rich CLI Guide[/] — pick a topic to explore

  [1] Console     — print, colors, clear screen
  [2] Panel       — bordered boxes with titles
  [3] Table       — rows and columns
  [4] Style & Text — colors, bold, styled segments
  [5] Align       — center content inside a box
  [6] Layout      — split the screen into regions
  [7] Live        — update the display in real time
  [8] Prompt      — ask the user for input
  [9] Resources   — docs, links, starter template
  [0] Quit
"""


def pause() -> None:
    console.print()
    Prompt.ask("[dim]Press Enter to return to the menu[/]", default="")


def demo_console() -> None:
    console.rule("[bold]1. Console[/]")
    console.print(
        "\n[bold]Console[/] is the starting point. Create one object and "
        "use it for all output.\n"
    )

    console.print("Plain text")
    console.print("[bold red]Bold red[/]  [italic green]Italic green[/]")
    console.print("[cyan underline]Underlined cyan[/]")

    console.print("\n[dim]console.print() accepts markup in square brackets:[/]")
    console.print("  [yellow]style[/] = [bold]bold[/] | [italic]italic[/] | "
                  "[dim]dim[/] | [reverse]reverse[/]")

    if Confirm.ask("\nTry clearing the screen?", default=False):
        console.clear()
        console.print("[green]Screen cleared with console.clear()[/]")

    console.print(Panel(
        "[white]console.print()[/] also accepts Rich objects like "
        "Panel, Table, and Text — not just strings.",
        title="Key idea",
        border_style="green",
    ))


def demo_panel() -> None:
    console.rule("[bold]2. Panel[/]")
    console.print(
        "\n[bold]Panel[/] wraps content in a bordered box. "
        "Great for sections, cards, and dashboard tiles.\n"
    )

    console.print(Panel("Simple message", title="Hello", border_style="blue"))

    inner = Table(show_header=False, box=None)
    inner.add_column("Key", style="cyan")
    inner.add_column("Action")
    inner.add_row("a", "add task")
    inner.add_row("q", "quit")
    console.print(Panel(inner, title="Shortcuts", border_style="magenta"))

    console.print(Panel(
        "[dim]Common args:[/]\n"
        "  title=          label on top border\n"
        "  border_style=   color of the border\n"
        "  expand=True     use full terminal width",
        title="Panel cheat sheet",
        border_style="yellow",
    ))


def demo_table() -> None:
    console.rule("[bold]3. Table[/]")
    console.print(
        "\n[bold]Table[/] builds a grid. Add columns, then rows.\n"
    )

    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Task", style="white")
    table.add_column("Due", justify="right", style="green")

    table.add_row("1", "Finish Rich guide", "05/30/26")
    table.add_row("2", "Study for exam", "06/02/26")
    table.add_row("3", "Push to GitHub", "06/01/26")

    console.print(Panel(table, title="Task List", border_style="blue"))

    console.print(Panel(
        "[dim]Workflow:[/]\n"
        "  table = Table(...)\n"
        "  table.add_column('Name', style='white')\n"
        "  table.add_row('value1', 'value2')\n\n"
        "  box=None removes inner grid lines for a cleaner list look.",
        title="Table cheat sheet",
        border_style="yellow",
    ))


def demo_style_and_text() -> None:
    console.rule("[bold]4. Style & Text[/]")
    console.print(
        "\nTwo ways to style output:\n"
        "  • [bold]Markup strings[/]: [bold cyan]'[bold cyan]Hello[/]'[/]\n"
        "  • [bold]Style objects[/]: reusable, built in code\n"
    )

    reusable = Style(color="cyan", bold=True)
    console.print("Built with Style object:", style=reusable)

    message = Text()
    message.append("[a]", style="bold cyan")
    message.append(" add  |  ", style="dim")
    message.append("[q]", style="bold red")
    message.append(" quit", style="dim")
    console.print(Panel(message, title="Text.append() — mixed styles in one line"))

    console.print(Panel(
        "Style(color='red', bold=True)\n"
        "Style(bgcolor='white', color='black')  # reverse highlight\n"
        "Column style: table.add_column('Due', style='cyan')",
        title="Style cheat sheet",
        border_style="yellow",
    ))


def demo_align() -> None:
    console.rule("[bold]5. Align[/]")
    console.print(
        "\n[bold]Align[/] positions content inside a Panel or Layout region.\n"
    )

    timer_text = Align.center(
        "\n[bold white]25:00[/]\n",
        vertical="middle",
    )
    console.print(Panel(timer_text, title="Timer", border_style="blue", height=7))

    empty_state = Align.center(
        "\n[italic grey42]No tasks yet[/]\n[grey30]Press [a] to add one[/]",
        vertical="middle",
    )
    console.print(Panel(empty_state, title="Task List", border_style="blue", height=7))


def demo_layout() -> None:
    console.rule("[bold]6. Layout[/]")
    console.print(
        "\n[bold]Layout[/] divides the terminal into named regions. "
        "Update each region with Panel, Table, or Text.\n"
    )

    layout = Layout()
    layout.split_column(
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(
        Layout(name="left", ratio=2),
        Layout(name="right", ratio=1),
    )

    layout["left"].update(Panel("Tasks go here", title="Left", border_style="blue"))
    layout["right"].update(Panel("Timer here", title="Right", border_style="green"))
    layout["footer"].update(
        Panel(Align.center("[a] add  |  [q] quit"), border_style="white")
    )

    console.print(layout)

    console.print(Panel(
        "layout = Layout()\n"
        "layout.split_column(Layout(name='main'), Layout(name='footer', size=3))\n"
        "layout['main'].update(Panel(...))\n\n"
        "Use split_row / split_column for responsive dashboards.",
        title="Layout cheat sheet",
        border_style="yellow",
    ))


def demo_live() -> None:
    console.rule("[bold]7. Live[/]")
    console.print(
        "\n[bold]Live[/] refreshes a region on a timer — perfect for "
        "countdowns, progress, or dashboards.\n"
    )

    seconds = IntPrompt.ask("Demo countdown seconds", default=5)
    layout = Layout()
    layout.update(Panel("", title="Live Timer", border_style="cyan"))

    with Live(layout, refresh_per_second=4, transient=True) as live:
        for remaining in range(seconds, -1, -1):
            mins, secs = divmod(remaining, 60)
            display = Align.center(
                f"\n[bold white]{mins:02d}:{secs:02d}[/]\n",
                vertical="middle",
            )
            layout.update(Panel(display, title="Live Timer", border_style="cyan"))
            live.refresh()
            if remaining > 0:
                time.sleep(1)

    console.print("[green]Live session ended.[/] transient=True removes it "
                  "when done.")


def demo_prompt() -> None:
    console.rule("[bold]8. Prompt[/]")
    console.print(
        "\n[bold]Prompt[/] collects input with styled questions — nicer "
        "than plain input().\n"
    )

    name = Prompt.ask("[yellow]Your name[/]", default="Student")
    age = IntPrompt.ask("[yellow]Your age[/]", default=20)

    console.print(Panel(
        f"Hello, [bold cyan]{name}[/]! You entered age [green]{age}[/].\n\n"
        "Prompt.ask()      → string\n"
        "IntPrompt.ask()   → integer (validates for you)\n"
        "Confirm.ask()     → yes / no boolean",
        title="Prompt result",
        border_style="green",
    ))


def show_resources() -> None:
    console.rule("[bold]9. Resources[/]")
    console.print(Markdown(RESOURCES))


DEMOS = {
    1: ("Console", demo_console),
    2: ("Panel", demo_panel),
    3: ("Table", demo_table),
    4: ("Style & Text", demo_style_and_text),
    5: ("Align", demo_align),
    6: ("Layout", demo_layout),
    7: ("Live", demo_live),
    8: ("Prompt", demo_prompt),
    9: ("Resources", show_resources),
}


def main() -> None:
    console.print(Panel(
        Align.center(
            "[bold]Build a Rich CLI in 4 steps[/]\n\n"
            "1. Create a [cyan]Console()[/]\n"
            "2. Compose UI with [cyan]Panel[/], [cyan]Table[/], [cyan]Text[/]\n"
            "3. Organize the screen with [cyan]Layout[/] (+ [cyan]Live[/] to refresh)\n"
            "4. Handle input with [cyan]Prompt[/] inside a [cyan]main()[/] loop",
            vertical="middle",
        ),
        title="Welcome",
        border_style="bold blue",
        padding=(1, 2),
    ))

    while True:
        console.print()
        console.print(MENU)
        choice = IntPrompt.ask("\n[bold]Choose a topic[/]", default=0)

        if choice == 0:
            console.print("\n[dim]Good luck with your CLI project![/]\n")
            break

        demo = DEMOS.get(choice)
        if demo is None:
            console.print("[red]Invalid choice. Pick 0–9.[/]")
            continue

        console.print()
        demo[1]()
        if choice != 9:
            pause()


if __name__ == "__main__":
    main()

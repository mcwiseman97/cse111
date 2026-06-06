import json
import pytest
from rich.align import Align
from rich.layout import Layout
from rich.table import Table
from rich.console import Console

import chronos

@pytest.fixture
def tasks_file(tmp_path, monkeypatch):
    """Point chronos at a temporary tasks.json for isolated file tests."""
    path = tmp_path / "tasks.json"
    monkeypatch.setattr(chronos, "DATA_FILE", str(path))
    return path


def capture_render(renderable):
    """Render a Rich object to plain text for easy assertions."""
    console = Console(width=80)
    with console.capture() as capture:
        console.print(renderable)
    return capture.get()


# --- format_date ---

def test_format_date_converts_iso_to_display():
    assert chronos.format_date("2025-06-15") == "06/15/25"


def test_format_date_returns_original_on_invalid_input():
    assert chronos.format_date("not-a-date") == "not-a-date"


# --- load_tasks / save_tasks ---

def test_load_tasks_returns_empty_when_file_missing(tasks_file):
    assert chronos.load_tasks() == []


def test_save_and_load_tasks_round_trip(tasks_file):
    sample = [{"name": "Study", "due": "2025-06-15"}]
    chronos.save_tasks(sample)
    assert chronos.load_tasks() == sample


def test_load_tasks_returns_empty_when_file_corrupted(tasks_file):
    tasks_file.write_text("{ broken json", encoding="utf-8")
    assert chronos.load_tasks() == []


# --- render_tasks ---

def test_render_tasks_empty_returns_align():
    result = chronos.render_tasks([])
    assert isinstance(result, Align)


def test_render_tasks_populated_returns_table():
    result = chronos.render_tasks([{"name": "Read", "due": "2025-06-01"}])
    assert isinstance(result, Table)


def test_render_tasks_sorts_by_due_date():
    tasks = [
        {"name": "Later", "due": "2025-12-01"},
        {"name": "Soon", "due": "2025-06-01"},
    ]
    chronos.render_tasks(tasks)
    assert tasks[0]["name"] == "Soon"
    assert tasks[1]["name"] == "Later"


def test_render_tasks_shows_formatted_dates():
    output = capture_render(
        chronos.render_tasks([{"name": "Homework", "due": "2025-03-04"}])
    )
    assert "Homework" in output
    assert "03/04/25" in output


# --- render_timer ---

def test_render_timer_formats_minutes_and_seconds():
    output = capture_render(chronos.render_timer(125))
    assert "02:05" in output


def test_render_timer_zero_seconds():
    output = capture_render(chronos.render_timer(0))
    assert "00:00" in output


def test_render_timer_full_hour():
    output = capture_render(chronos.render_timer(3600))
    assert "60:00" in output


# --- make_dashboard ---

def test_make_dashboard_returns_layout_with_sections():
    layout = chronos.make_dashboard([], 1500)
    assert isinstance(layout, Layout)
    assert layout["tasks_box"] is not None
    assert layout["timer_box"] is not None
    assert layout["footer"] is not None


# --- add_task / complete_task ---

def test_add_task_appends_and_saves(tasks_file, monkeypatch):
    tasks = []
    responses = iter(["Homework", "06/15/25"])
    monkeypatch.setattr(chronos.Prompt, "ask", lambda prompt, **kw: next(responses))
    monkeypatch.setattr(chronos, "enable_key_mode", lambda: None)

    chronos.add_task(tasks, None)

    assert tasks == [{"name": "Homework", "due": "2025-06-15"}]
    assert json.loads(tasks_file.read_text(encoding="utf-8")) == tasks


def test_add_task_uses_today_on_bad_date(tasks_file, monkeypatch):
    tasks = []
    responses = iter(["Bad date task", "not-valid"])
    monkeypatch.setattr(chronos.Prompt, "ask", lambda prompt, **kw: next(responses))
    monkeypatch.setattr(chronos, "enable_key_mode", lambda: None)

    chronos.add_task(tasks, None)

    assert len(tasks) == 1
    assert tasks[0]["name"] == "Bad date task"
    assert len(tasks[0]["due"]) == 10  # YYYY-MM-DD


def test_complete_task_removes_selected_task(tasks_file, monkeypatch):
    tasks = [
        {"name": "First", "due": "2025-06-01"},
        {"name": "Second", "due": "2025-12-01"},
    ]
    monkeypatch.setattr(chronos.IntPrompt, "ask", lambda *args, **kw: 1)
    monkeypatch.setattr(chronos.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(chronos, "enable_key_mode", lambda: None)

    chronos.complete_task(tasks, None)

    assert tasks == [{"name": "Second", "due": "2025-12-01"}]


def test_complete_task_zero_choice_keeps_tasks(monkeypatch):
    tasks = [{"name": "Keep me", "due": "2025-06-01"}]
    monkeypatch.setattr(chronos.IntPrompt, "ask", lambda *args, **kw: 0)
    monkeypatch.setattr(chronos.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(chronos, "enable_key_mode", lambda: None)

    chronos.complete_task(tasks, None)

    assert tasks == [{"name": "Keep me", "due": "2025-06-01"}]


# --- start_timer ---

def test_start_timer_returns_zero_when_already_finished(monkeypatch):
    monkeypatch.setattr(chronos, "key_pressed", lambda: False)
    monkeypatch.setattr(chronos.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(chronos.notification, "notify", lambda **kwargs: None)

    result = chronos.start_timer([], 0)

    assert result == 0


pytest.main(["-v", "--tb=line", "-rN", __file__])

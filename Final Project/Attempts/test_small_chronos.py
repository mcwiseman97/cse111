import json
import pytest

import small_chronos


@pytest.fixture
def tasks_file(tmp_path, monkeypatch):
    path = tmp_path / "small_tasks.json"
    monkeypatch.setattr(small_chronos, "DATA_FILE", str(path))
    return path


# --- format_date / parse_due_date ---

def test_format_date_converts_iso_to_display():
    assert small_chronos.format_date("2025-06-15") == "06/15/25"


def test_format_date_returns_original_on_invalid_input():
    assert small_chronos.format_date("not-a-date") == "not-a-date"


def test_parse_due_date_converts_user_input():
    assert small_chronos.parse_due_date("06/15/25") == "2025-06-15"


def test_parse_due_date_uses_today_on_invalid_input():
    result = small_chronos.parse_due_date("bad-date")
    assert len(result) == 10
    assert result[4] == "-"


# --- load_tasks / save_tasks ---

def test_load_tasks_returns_empty_when_file_missing(tasks_file):
    assert small_chronos.load_tasks() == []


def test_save_and_load_tasks_round_trip(tasks_file):
    sample = [{"name": "Study", "due": "2025-06-15"}]
    small_chronos.save_tasks(sample)
    assert small_chronos.load_tasks() == sample


def test_load_tasks_returns_empty_when_file_corrupted(tasks_file):
    tasks_file.write_text("{ broken json", encoding="utf-8")
    assert small_chronos.load_tasks() == []


# --- format_timer ---

def test_format_timer_formats_minutes_and_seconds():
    assert small_chronos.format_timer(125) == "02:05"


def test_format_timer_zero_seconds():
    assert small_chronos.format_timer(0) == "00:00"


def test_format_timer_full_hour():
    assert small_chronos.format_timer(3600) == "60:00"


# --- get_task_lines ---

def test_get_task_lines_empty():
    assert small_chronos.get_task_lines([]) == ["No tasks yet."]


def test_get_task_lines_sorted_and_formatted():
    tasks = [
        {"name": "Later", "due": "2025-12-01"},
        {"name": "Soon", "due": "2025-06-01"},
    ]
    lines = small_chronos.get_task_lines(tasks)
    assert lines[0] == "1. Soon  Due: 06/01/25"
    assert lines[1] == "2. Later  Due: 12/01/25"


# --- add_task / complete_task ---

def test_add_task_appends_and_saves(tasks_file, monkeypatch):
    tasks = []
    inputs = iter(["Homework", "06/15/25"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    small_chronos.add_task(tasks)

    assert tasks == [{"name": "Homework", "due": "2025-06-15"}]
    assert json.loads(tasks_file.read_text(encoding="utf-8")) == tasks


def test_add_task_rejects_empty_name(monkeypatch):
    tasks = []
    monkeypatch.setattr("builtins.input", lambda prompt="": "")

    small_chronos.add_task(tasks)

    assert tasks == []


def test_complete_task_removes_selected_task(tasks_file, monkeypatch):
    tasks = [
        {"name": "First", "due": "2025-06-01"},
        {"name": "Second", "due": "2025-12-01"},
    ]
    monkeypatch.setattr("builtins.input", lambda prompt="": "1")

    small_chronos.complete_task(tasks)

    assert tasks == [{"name": "Second", "due": "2025-12-01"}]


def test_complete_task_zero_choice_keeps_tasks(monkeypatch):
    tasks = [{"name": "Keep me", "due": "2025-06-01"}]
    monkeypatch.setattr("builtins.input", lambda prompt="": "0")

    small_chronos.complete_task(tasks)

    assert tasks == [{"name": "Keep me", "due": "2025-06-01"}]


def test_complete_task_handles_invalid_number(monkeypatch):
    tasks = [{"name": "Keep me", "due": "2025-06-01"}]
    monkeypatch.setattr("builtins.input", lambda prompt="": "9")

    small_chronos.complete_task(tasks)

    assert tasks == [{"name": "Keep me", "due": "2025-06-01"}]


# --- start_timer ---

def test_start_timer_counts_down_and_returns_zero(monkeypatch):
    slept = []
    monkeypatch.setattr(small_chronos.time, "sleep", lambda seconds: slept.append(seconds))

    result = small_chronos.start_timer(3)

    assert result == 0
    assert slept == [1, 1, 1]


pytest.main(["-v", "--tb=line", "-rN", __file__])

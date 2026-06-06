import os

import pytest

from expense_tracker import (
    calculate_category_total,
    calculate_monthly_total,
    load_transactions,
    parse_amount,
    save_transactions,
)


SAMPLE_TRANSACTIONS = [
    {"date": "6-1-26", "category": "food", "description": "groceries", "amount": 45.50},
    {"date": "6-2-26", "category": "gas", "description": "fill-up", "amount": 38.00},
    {"date": "6-3-26", "category": "food", "description": "lunch", "amount": 12.25},
    {"date": "5-28-26", "category": "fun", "description": "movie", "amount": 15.00},
]


def test_calculate_category_total():
    """Verify that calculate_category_total works correctly."""
    assert calculate_category_total(SAMPLE_TRANSACTIONS, "food") == 57.75
    assert calculate_category_total(SAMPLE_TRANSACTIONS, "gas") == 38.00
    assert calculate_category_total(SAMPLE_TRANSACTIONS, "rent") == 0.0
    assert calculate_category_total([], "food") == 0.0


def test_calculate_monthly_total():
    """Verify that calculate_monthly_total works correctly."""
    assert calculate_monthly_total(SAMPLE_TRANSACTIONS, 2026, 6) == 95.75
    assert calculate_monthly_total(SAMPLE_TRANSACTIONS, 2026, 5) == 15.00
    assert calculate_monthly_total(SAMPLE_TRANSACTIONS, 2026, 4) == 0.0
    assert calculate_monthly_total([], 2026, 6) == 0.0


def test_parse_amount():
    """Verify that parse_amount works correctly."""
    assert parse_amount("45.50") == 45.50
    assert parse_amount("$12.34") == 12.34
    assert parse_amount("  8  ") == 8.0

    with pytest.raises(ValueError):
        parse_amount("abc")

    with pytest.raises(ValueError):
        parse_amount("-5.00")


def test_save_and_load_transactions():
    """Verify that save_transactions and load_transactions work correctly."""
    filename = "test_expenses.csv"
    save_transactions(filename, SAMPLE_TRANSACTIONS)

    loaded = load_transactions(filename)
    os.remove(filename)

    assert len(loaded) == len(SAMPLE_TRANSACTIONS)
    assert loaded[0]["category"] == "food"
    assert loaded[0]["amount"] == 45.50
    assert loaded[1]["description"] == "fill-up"


pytest.main(["-v", "--tb=line", "-rN", __file__])

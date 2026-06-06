import csv
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "expenses.csv")
CSV_HEADERS = ["date", "category", "description", "amount"]
VALID_CATEGORIES = ["food", "gas", "rent", "fun", "other"]
DATE_FORMAT = "%m-%d-%y"


def parse_amount(text):
    cleaned = text.strip().replace("$", "").replace(",", "")
    amount = float(cleaned)
    if amount < 0:
        raise ValueError("Amount must be zero or greater.")
    return round(amount, 2)

def format_money(amount):
    return f"${amount:.2f}"


def format_date(date_obj):
    """Format a datetime as M-D-YY, such as 5-19-26."""
    return f"{date_obj.month}-{date_obj.day}-{date_obj.strftime('%y')}"


def parse_date(text):
    """Parse an M-D-YY date string and return it in normalized form.

    Parameters
        text: a date string such as 5-19-26 or 06-01-26
    Return: a normalized date string such as 5-19-26
    """
    date_obj = datetime.strptime(text.strip(), DATE_FORMAT)
    return format_date(date_obj)


def date_to_datetime(date_str):
    """Convert a stored date string to a datetime object."""
    return datetime.strptime(date_str, DATE_FORMAT)


def calculate_category_total(transactions, category):
    total = 0.0
    category = category.lower()
    for transaction in transactions:
        if transaction["category"].lower() == category:
            total += float(transaction["amount"])
    return round(total, 2)

def calculate_monthly_total(transactions, year, month):
    total = 0.0
    for transaction in transactions:
        date_obj = date_to_datetime(transaction["date"])
        if date_obj.year == year and date_obj.month == month:
            total += float(transaction["amount"])
    return round(total, 2)

def calculate_percent_of_total(amount, total):
    if total == 0:
        return 0.0
    return round((amount / total) * 100, 1)

def get_unique_categories(transactions):
    categories = set()
    for transaction in transactions:
        categories.add(transaction["category"].lower())
    return sorted(categories)

def load_transactions(filename):
    if not os.path.exists(filename):
        return []

    transactions = []
    with open(filename, "rt", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            transactions.append({
                "date": row["date"],
                "category": row["category"],
                "description": row["description"],
                "amount": float(row["amount"]),
            })
    return transactions

def save_transactions(filename, transactions):

    with open(filename, "wt", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for transaction in transactions:
            writer.writerow({
                "date": transaction["date"],
                "category": transaction["category"],
                "description": transaction["description"],
                "amount": f"{float(transaction['amount']):.2f}",
            })

def display_summary(transactions):

    if not transactions:
        print("\nNo transactions recorded yet.")
        return

    print("\n--- Expense Summary ---")
    categories = get_unique_categories(transactions)
    category_totals = {}
    grand_total = 0.0
    for category in categories:
        category_total = calculate_category_total(transactions, category)
        category_totals[category] = category_total
        grand_total += category_total

    for category in categories:
        category_total = category_totals[category]
        percent = calculate_percent_of_total(category_total, grand_total)
        print(
            f"{category.title():<10} "
            f"{format_money(category_total):>10} "
            f"({percent:.1f}%)"
        )

    if grand_total > 0:
        print("-" * 30)
        print(f"{'Total':<10} {format_money(grand_total):>10}")

    now = datetime.now()
    month_total = calculate_monthly_total(transactions, now.year, now.month)
    month_name = now.strftime("%B %Y")
    print(f"\nSpent this month ({month_name}): {format_money(month_total)}")

def add_transaction_interactive(transactions):
    print("\nAdd a new expense")
    print(f"Categories: {', '.join(VALID_CATEGORIES)}")
    category = input("Category: ").strip().lower()

    while category not in VALID_CATEGORIES:
        print(f"Please enter one of: {', '.join(VALID_CATEGORIES)}")
        category = input("Category: ").strip().lower()

    description = input("Description: ").strip()
    while description == "":
        print("Description cannot be empty.")
        description = input("Description: ").strip()

    amount_text = input("Amount: ").strip()
    amount = None
    while amount is None:
        try:
            amount = parse_amount(amount_text)
        except ValueError:
            print("Please enter a valid dollar amount, such as 12.50")
            amount_text = input("Amount: ").strip()

    date_text = input(
        "Date (M-D-YY, press Enter for today): "
    ).strip()
    if date_text == "":
        date_text = format_date(datetime.now())
    else:
        try:
            date_text = parse_date(date_text)
        except ValueError:
            print("Invalid date format. Use M-D-YY, such as 5-19-26.")
            date_text = format_date(datetime.now())

    transactions.append({
        "date": date_text,
        "category": category,
        "description": description,
        "amount": amount,
    })
    save_transactions(DATA_FILE, transactions)
    print(f"Saved: {description} - {format_money(amount)}")

def main():
    transactions = load_transactions(DATA_FILE)

    while True:
        print("\nPersonal Expense Tracker")
        print("1. Add expense")
        print("2. View summary")
        print("3. Quit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            add_transaction_interactive(transactions)
        elif choice == "2":
            display_summary(transactions)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

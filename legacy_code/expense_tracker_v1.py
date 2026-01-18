# expense_tracker version 1 week 1, 15/11/25
# week 1 deliverable (simple CLI based application)

import csv
from datetime import date

def add_expense(expenses):
    print(f"\n\tAdd a new expense")
    d = input('Enter date(YYYY-MM-DD, leave blank for today): ').strip() #enter the date of the expense, and if empty, enter tpdays date
    if not d:
        d = str(date.today()) # convert the date to a string

    while True:
        category = input('Category(food, transport, rent, bills, health, other: )').strip().lower()
        if category not in ('food', 'transport', 'rent', 'bills', 'health', 'other'):
            print('Not valid, please choose an option as mentioned.')
        else:
            break
    while True:
        amt_str = input('Amount: ').strip()
        try:
            amt = float(amt_str)
            break
        except ValueError:
            print('Please enter a valid amount.')
        
    desc = input('Description (optional): ').strip()
    expenses.append({
        "date": d,
        "category": category,
        "amount": amt,
        "description": desc
    })
    print('Expense Added')

def list_expenses(expenses):

    if not expenses:
        print('\nNo expenses to display.')
        return
    print('\t\n-------Expenses------')
    for i, e in enumerate(expenses, start=1):
        print(f"{i}. {e['date']} | {e['category']} | {e['amount']:.2f} | {e['description']}")

def show_total(expenses):
    total = sum(e['amount']for e in expenses)
    print(f"Total amounnt: {total:.2f}")

def save_to_csv(expenses, filename="expenses.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "description"])
        writer.writeheader()
        for e in expenses:
            writer.writerow(e)
    print(f"\nSaved {len(expenses)} expense(s) to {filename}")




    



    
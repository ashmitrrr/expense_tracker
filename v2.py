# expense_tracker version 2 week: 30th nov
# pandas and matplotlib added week 2 deliverable


import csv
from datetime import date
import pandas as pd

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

def load_expenses(filename="expenses.csv"):
    '''
    we are going to load the csv created by v1, into a pandas dataframe.
    return the data frame, or none if the file does not exist.
    '''
    try:
        df = pd.read_csv(filename, parse_dates=["date"])
        return df
    except FileNotFoundError:
        print(f"File {filename} not found. Run v1 and save some expenses.")
        return None
    
def summary(df):
    print('======SUMMARY========')
    num_expenses = len(df)
    print(f'Number of expenses: {num_expenses}')

    total_spent= df['amount'].sum()
    print(f'Total amount of expenses so far: {total_spent:.2f}')

def category_summary(df):
    print(f'=====SPENDING BY CATEGORY=====')
    category_total = df.groupby('category')['amount'].sum()
    print(category_total)



def main():
    df = load_expenses()
    if df is None:
        return
    
    print('\n--------Table---------')
    print(df)

    print(f'\n=======First 5 rows=======')
    print(df.head())

    summary(df)
    category_summary(df)

if __name__=='__main__':
    main()
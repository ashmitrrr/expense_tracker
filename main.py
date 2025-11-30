from expense_tracker_v1 import add_expense, list_expenses, show_total, save_to_csv 


def main():
    expenses = []
    print('\n\tExpense Tracker V1')
    while True:
        print('\n1) ADD EXPENSE')
        print('\n2) LIST EXPENSES')
        print('\n3) SHOW TOTAL')
        print('\n4) SAVE AND EXIT')
        choice = input('Choose an option number (1,2,3,4): ').strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            show_total(expenses)
        elif choice == "4":
            save_to_csv(expenses)
            break
        else:
            print("Invalid choice. Try 1-4.")
    
if __name__ == "__main__":
    main()
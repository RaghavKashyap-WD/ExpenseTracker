import os
from expense import Expense
import calendar
import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

DB_USER =   os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")


engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")


def main():
    print(f"🎯 Running Expense Tracker!")   
    expense_file_path = "expense.csv"
    budget = 50000  # Example budget, you can change this as needed
    print(f"💰 Your Monthly Budget: ₹{budget}")

    # Get user input for expense
    expense = get_user_input()

    # store that to SQL DB
    save_expense(expense)

    # Read file and Summarize expeses
    summarize(budget)
    


def get_user_input():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name:")
    expense_amount = float(input("Enter expense amount:"))
    print(f"You have entered {expense_name}, {expense_amount}")

    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while(True):
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i+1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a ctegory number {value_range}:")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")



def save_expense(expense: Expense):
    print(f"🎯 Saving user expense")
    df = pd.DataFrame([{
        "name": expense.name,
        "amount": expense.amount,
        "category": expense.category
    }])
    df.to_sql(TABLE_NAME, con=engine, if_exists="append", index=False)


def summarize(budget):
    print(f"🎯 Summarizing user expense")
    df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", con=engine)

    if df.empty:
        print("No expenses found.")
        return

    grouped = df.groupby("category")["amount"].sum()

    print("Expenses By Category 📈:")
    for category, amount in grouped.items():
        print(f"  {category}: ₹{amount:.2f}")

    total_spent = df["amount"].sum()
    print(f"💵 Total Spent: ₹{total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ₹{remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days if remaining_days else 0
    print(green(f"👉 Budget Per Day: ₹{daily_budget:.2f}"))


def green(text):
    return f"\033[92m{text}\033[0m"


if __name__ == "__main__":
    main()
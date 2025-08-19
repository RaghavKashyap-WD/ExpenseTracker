# Expense Tracker Application
# A comprehensive expense tracking system that allows users to record, categorize, and analyze their spending habits
# This application uses MySQL database for persistent storage and provides budget tracking features

# Required imports for the application functionality
import os                     # For environment variable access
from expense import Expense   # Custom Expense class for expense objects
import calendar               # For calendar-related calculations (days in month)
import datetime               # For date and time operations
import pandas as pd           # For data manipulation and analysis
from sqlalchemy import create_engine  # For database connection and operations
from dotenv import load_dotenv        # For loading environment variables from .env file

# Load environment variables from .env file
# This allows secure storage of database credentials without hardcoding them
load_dotenv()

# Database configuration - retrieved from environment variables for security
DB_USER = os.getenv("DB_USER")         # MySQL database username
DB_PASSWORD = os.getenv("DB_PASSWORD") # MySQL database password
DB_HOST = os.getenv("DB_HOST")         # MySQL database host address
DB_NAME = os.getenv("DB_NAME")         # MySQL database name
TABLE_NAME = os.getenv("TABLE_NAME")   # Table name for storing expenses

# Create database engine for MySQL connection
# Uses SQLAlchemy to establish connection with MySQL database using mysqlconnector
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

def main():
    """
    Main function that orchestrates the expense tracking workflow
    
    This function:
    1. Initializes the application with welcome message
    2. Sets the monthly budget (currently hardcoded but can be made configurable)
    3. Gets expense input from user
    4. Saves the expense to database
    5. Provides expense summary and budget analysis
    
    Input: None
    Output: Prints various status messages and expense summaries
    """
    print(f"🎯 Running Expense Tracker!")   
    
    # File path for potential CSV backup (currently unused but kept for future enhancement)
    expense_file_path = "expense.csv"
    
    # Monthly budget in rupees - this could be made configurable in future versions
    budget = 50000  # Example budget, you can change this as needed
    print(f"💰 Your Monthly Budget: ₹{budget}")
    
    # Get user input for expense details (name, amount, category)
    expense = get_user_input()
    
    # Store the expense data to SQL database for persistence
    save_expense(expense)
    
    # Generate and display expense summary with budget analysis
    summarize(budget)

def get_user_input():
    """
    Collects expense information from user through interactive prompts
    
    This function:
    1. Prompts user for expense name and amount
    2. Displays available expense categories
    3. Validates user's category selection
    4. Creates and returns an Expense object
    
    Input: User input through console (expense name, amount, category selection)
    Output: Returns an Expense object containing user's expense data
    
    Validation: Ensures category selection is within valid range
    """
    print(f"🎯 Getting User Expense")
    
    # Get expense details from user
    expense_name = input("Enter expense name:")
    expense_amount = float(input("Enter expense amount:"))
    
    # Confirm entered details with user
    print(f"You have entered {expense_name}, {expense_amount}")
    
    # Predefined expense categories with emojis for better user experience
    expense_categories = [
        "🍔 Food",      # Food and dining expenses
        "🏠 Home",      # Home-related expenses (utilities, rent, maintenance)
        "💼 Work",      # Work-related expenses (commute, supplies, etc.)
        "🎉 Fun",       # Entertainment and leisure expenses
        "✨ Misc",      # Miscellaneous expenses that don't fit other categories
    ]
    
    # Category selection loop with validation
    while(True):
        print("Select a category: ")
        
        # Display all available categories with numbered options
        for i, category_name in enumerate(expense_categories):
            print(f"{i+1}. {category_name}")
        
        # Show valid input range to user
        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a ctegory number {value_range}:")) - 1
        
        # Validate user selection is within valid range
        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            
            # Create new Expense object with user's input
            new_expense = Expense(
                name=expense_name, 
                category=selected_category, 
                amount=expense_amount
            )
            return new_expense
        else:
            # Invalid selection - prompt user to try again
            print("Invalid category. Please try again!")

def save_expense(expense: Expense):
    """
    Saves expense data to MySQL database
    
    This function:
    1. Converts Expense object to pandas DataFrame
    2. Writes data to MySQL database table
    3. Appends to existing data without overwriting
    
    Input: expense (Expense object) - contains name, amount, and category
    Output: None (data is saved to database)
    
    Database operation: Appends new record to the specified table
    """
    print(f"🎯 Saving user expense")
    
    # Convert expense object to pandas DataFrame for database insertion
    # DataFrame structure matches database table schema
    df = pd.DataFrame([{
        "name": expense.name,        # Expense description/name
        "amount": expense.amount,    # Expense amount in rupees
        "category": expense.category # Expense category
    }])
    
    # Save DataFrame to MySQL database
    # if_exists="append" ensures new data is added without overwriting existing records
    # index=False prevents pandas index from being saved as a column
    df.to_sql(TABLE_NAME, con=engine, if_exists="append", index=False)

def summarize(budget):
    """
    Generates comprehensive expense summary and budget analysis
    
    This function:
    1. Retrieves all expenses from database
    2. Groups expenses by category and calculates totals
    3. Displays category-wise spending breakdown
    4. Shows total spending and remaining budget
    5. Calculates daily budget for remaining days in month
    
    Input: budget (float) - monthly budget amount in rupees
    Output: Prints detailed expense summary and budget analysis
    
    Features:
    - Category-wise expense breakdown
    - Total spending calculation
    - Remaining budget calculation
    - Daily budget recommendation for remaining days
    """
    print(f"🎯 Summarizing user expense")
    
    # Retrieve all expense records from database
    df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", con=engine)
    
    # Check if any expenses exist
    if df.empty:
        print("No expenses found.")
        return
    
    # Group expenses by category and sum amounts for each category
    grouped = df.groupby("category")["amount"].sum()
    
    # Display category-wise expense breakdown
    print("Expenses By Category 📈:")
    for category, amount in grouped.items():
        print(f"  {category}: ₹{amount:.2f}")
    
    # Calculate and display total spending
    total_spent = df["amount"].sum()
    print(f"💵 Total Spent: ₹{total_spent:.2f}")
    
    # Calculate and display remaining budget
    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ₹{remaining_budget:.2f}")
    
    # Calculate daily budget recommendation for remaining days in current month
    now = datetime.datetime.now()
    # Get total days in current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    # Calculate remaining days in current month
    remaining_days = days_in_month - now.day
    
    # Calculate daily budget (avoid division by zero)
    daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0
    print(green(f"👉 Budget Per Day: ₹{daily_budget:.2f}"))

def green(text):
    """
    Utility function to format text in green color for console output
    
    This function uses ANSI escape codes to colorize text in terminal
    Green color is used to highlight positive information like budget recommendations
    
    Input: text (string) - text to be colored
    Output: Returns formatted string with green color codes
    
    ANSI codes used:
    - \033[92m: Start green text
    - \033[0m: Reset to default color
    """
    return f"\033[92m{text}\033[0m"

# Application entry point
# This ensures the main() function only runs when script is executed directly
# (not when imported as a module)
if __name__ == "__main__":
    main()

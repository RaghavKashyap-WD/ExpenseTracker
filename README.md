# 💸 ExpenseTracker

A simple and colorful command-line expense tracker built with Python and MySQL. This tool allows you to input your daily expenses, categorize them, and track your budget throughout the month with live summaries.

---

## ✨ Features

- ✅ Track and save expenses to a MySQL database
- 📊 Get a live summary grouped by category
- 📆 Calculates remaining budget and daily budget projection for the month
- ⚙️ Simple setup using environment variables and SQLAlchemy
- 🎨 Fun emoji‑based categories and color-coded output

---

## 🧰 Tech Stack

- **Python 3.7+**
- **MySQL**
- **SQLAlchemy**
- **pandas**
- **dotenv**

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/RaghavKashyap-WD/ExpenseTracker.git
cd ExpenseTracker


2. Install dependencies

Make sure you're in a virtual environment (python -m venv .venv recommended), then:

pip install pandas sqlalchemy mysql-connector-python python-dotenv

3. Setup .env file

Create a .env file in the root directory and add your MySQL credentials:

DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=your_database
TABLE_NAME=expenses

> ℹ️ This file is used to securely load database credentials using os.getenv() in Python (explained below).



4. Create the MySQL table

Log in to MySQL and run:

CREATE TABLE expenses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  amount DECIMAL(10,2),
  category VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


---

🚀 How to Run

python expense_tracker.py

You'll be prompted to enter:

•Expense name

•Amount

•Category (choose from Food, Home, Work, Fun, Misc)


Your data will be saved to the MySQL database

A summary will show:

Spending per category

Total spent

Remaining budget

Budget available per day




---

📂 Project Structure

ExpenseTracker/
├── .gitignore           # Ignoring envs, logs, and bytecode
├── .env                 # DB config (excluded from Git)
├── expense.py           # Defines the Expense class
├── expense_tracker.py   # Main logic and user interface
└── README.md            # You're reading it!


---

🤔 Why import os is used

In expense_tracker.py, the line:

import os

is used to:

Access environment variables securely, like DB credentials

Use os.getenv("DB_USER") to avoid hardcoding sensitive info

Keep your database safe, especially when committing code to GitHub


✅ This improves security, flexibility, and portability.


---

🎨 Screenshots (Sample Output)

🎯 Running Expense Tracker!
💰 Your Monthly Budget: ₹50000
Enter expense name: Coffee
Enter expense amount: 80
You have entered Coffee, 80.0
Select a category:
1. 🍔 Food
2. 🏠 Home
3. 💼 Work
4. 🎉 Fun
5. ✨ Misc
Enter a category number [1 - 5]: 1

🎯 Saving user expense
🎯 Summarizing user expense
Expenses By Category 📈:
  🍔 Food: ₹80.00
💵 Total Spent: ₹80.00
✅ Budget Remaining: ₹49920.00
👉 Budget Per Day: ₹1,713.79


---

🧪 To Customize

Change Monthly Budget:
Edit budget = 50000 in expense_tracker.py

Add More Categories:
Edit the expense_categories list in get_user_input()

Change Table Name:
Modify TABLE_NAME in .env



---

🤝 Contributing

If you’d like to improve this project:

1. Fork this repo


2. Make your changes


3. Open a pull request 🙌




---

📜 License

This project is open-source under the MIT License.


---

Made with ☕ and ❤️ by Raghav Kashyap

---
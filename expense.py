# Expense class represents a single expense item with name, amount, and category
class Expense:
    # Constructor method to initialize a new expense object
    def __init__(self, name, amount, category):
        # name: The description or title of the expense (e.g., "Coffee", "Gas")
        self.name = name
        # amount: The monetary value of the expense as a number
        self.amount = amount
        # category: The type or classification of the expense (e.g., "Food", "Transport")
        self.category = category

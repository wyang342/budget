from classes.budget_category import BudgetCategory
from classes.budget import Budget
import os
import csv


class BudgetInterface:

    def __init__(self):
        self.my_budget = Budget()

    def run(self):
        self.read_categories_from_csv()
        self.read_monthly_income_from_txt()
        print("Welcome to your budget manager.\n")

        while True:
            print("Please choose an option:")
            choice = input("1. Update your monthly income.\n2. Reveal my monthly costs.\n3. Create and calculate new expenses.\n4. Reveal what percent of my monthly income is being spent in each category.\n5. Quit\n> ")
            print()

            if choice == '1':
                monthly_income = input("What is your monthly income?\n")
                self.my_budget.monthly_income = monthly_income
                self.save_monthly_income_to_txt()
                print()
            elif choice == '2':
                self.reveal_monthly_costs()
                print()
            elif choice == '3':
                self.create_new_expenses()
            elif choice == '4':
                self.determine_percentages()
            elif choice == '5':
                print("Goodbye")
                break

    def create_new_expenses(self):
        while True:
            category_name = input("Enter your new budget category: ")
            monthly_expenses = input("Enter the monthly expenses: ")
            self.my_budget.budget_categories.append(
                BudgetCategory(category_name, monthly_expenses))

            should_continue = input("Enter more categories? (y)es : (n)o\n")
            print()
            if should_continue == 'n':
                self.save_budget_categories_to_csv()
                break
            elif should_continue == 'y':
                pass

    def reveal_monthly_costs(self):
        self.read_categories_from_csv()
        total_expenses = 0
        for category in self.my_budget.budget_categories:
            total_expenses += int(category.monthly_expenses)
            print(
                f"Category: {category.category_name}  |  Monthly Expenses: {category.monthly_expenses}")

        print(f"Total monthly expenses: {total_expenses}")

    def read_categories_from_csv(self):
        dir_path = os.path.abspath(os.getcwd())
        csv_path = os.path.join(dir_path, "data/monthly_expenses.csv")

        with open(csv_path) as csvfile:
            self.my_budget.budget_categories = []
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.my_budget.budget_categories.append(
                    BudgetCategory(**dict(row)))

    def read_monthly_income_from_txt(self):
        dir_path = os.getcwd()  # returns path to /budget
        txt_path = os.path.join(dir_path, "data/monthly_income.txt")

        with open(txt_path) as txtfile:
            line = txtfile.readline()
            self.my_budget.monthly_income = int(line)

    def determine_percentages(self):
        if int(self.my_budget.monthly_income) == 0:
            print("Please enter in your monthly income.")
            print()
            return

        for category in self.my_budget.budget_categories:
            percentage = (int(category.monthly_expenses) /
                          int(self.my_budget.monthly_income)) * 100
            print(
                f"Category: {category.category_name}  |  Percentage of total budget: {percentage}%")
        print()

    def save_budget_categories_to_csv(self):
        fields = ["category_name", "monthly_expenses"]

        dir_path = os.getcwd()  # returns path to /budget
        csv_path = os.path.join(dir_path, "data/monthly_expenses.csv")

        with open(csv_path, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(fields)
            for category in self.budget_categories:
                writer.writerow(
                    [category.category_name, category.monthly_expenses])

    def save_monthly_income_to_txt(self):
        dir_path = os.getcwd()  # returns path to /budget
        txt_path = os.path.join(dir_path, "data/monthly_income.txt")

        with open(txt_path, "w") as txtfile:
            txtfile.write(self.my_budget.monthly_income)

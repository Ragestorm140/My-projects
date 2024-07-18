from flask import Flask, render_template, request, redirect, url_for
from expense import Expense
import pandas as pd
import os
import calendar
import datetime

app = Flask(__name__)

# Fake budget data for demonstration
budget = 12000
expense_file_path = "expense.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        exp_name = request.form['exp_name']
        exp_category = request.form['exp_category']
        exp_amount_str = request.form['exp_amount']  # Get the string value of amount
        
        # Validate and convert the amount to float
        try:
            exp_amount = float(exp_amount_str)
        except ValueError:
            # If conversion fails, render the add_expense template with an error message
            error_message = 'Invalid expense amount. Please enter a valid number.'
            return render_template('add_expense.html', error_message=error_message)
        
        # If no error occurred, create Expense object and save it
        new_expense = Expense(name=exp_name, category=exp_category, amount=exp_amount)
        save_expense(new_expense, expense_file_path)
        return redirect(url_for('summary'))
    return render_template('add_expense.html')

@app.route('/summary')
def summary():
    expenses = load_expenses(expense_file_path)
    total_spent, amount_by_category, remaining_budget, avg_daily_budget, daily_limit = summarize_expense(expenses)
    return render_template('summary.html', total_spent=total_spent, amount_by_category=amount_by_category,
                           remaining_budget=remaining_budget, avg_daily_budget=avg_daily_budget,
                           daily_limit=daily_limit)

def save_expense(expense, expense_file_path):
    # Save expense to CSV file
    with open(expense_file_path, 'a') as filehandle:
        filehandle.write(f"{expense.name},{expense.amount},{expense.category}\n")

def load_expenses(expense_file_path):
    expenses = []
    with open(expense_file_path, 'r') as filehandle:
        lines = filehandle.readlines()
        for line in lines:
            exp_name, exp_amount, exp_category = line.strip().split(",")
            line_expense = Expense(name=exp_name, amount=float(exp_amount), category=exp_category)
            expenses.append(line_expense)
    return expenses

def summarize_expense(expenses):
    amount_by_category = {}
    total_spent = 0
    for expense in expenses:
        total_spent += expense.amount
        if expense.category in amount_by_category:
            amount_by_category[expense.category] += expense.amount
        else:
            amount_by_category[expense.category] = expense.amount

    remaining_budget = budget - total_spent
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    avg_daily_budget = total_spent / days_in_month
    remaining_days = days_in_month - now.day
    daily_limit = remaining_budget / remaining_days
    return total_spent, amount_by_category, remaining_budget, avg_daily_budget, daily_limit

if __name__ == '__main__':
    app.run(debug=True)

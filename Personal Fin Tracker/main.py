"""

Personal Finance tracker --> input {
    Expenses
    Income
    Saving
    
    if expense or saving --> - from total
    else +
    
    store in json file at date
}

"""

import json
from datetime import datetime
from pathlib import Path

JSON_FILE = Path(__file__).parent / "Tracking.json"



def store_data(amount, type, desc):
    try:
        with open(JSON_FILE, "r") as json_file:
            data_list = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data_list = []

    data_list.append({
        "Amount" : amount,
        "Type" : type,
        "Description" : desc,
        "Date" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(JSON_FILE, "w") as json_file:
        json.dump(data_list, json_file, indent=4)

    print("Data successfully appended!")



def expenses():
    amount = int(input("Enter the amount of expense: "))
    desc = input("Enter the description of the expense: ")
    store_data(amount, "Expense", desc)

    
def income():
    amount = int(input("Enter the amount of income: "))
    desc = input("Enter the description of the income: ")
    store_data(amount, "Income", desc)
    
def saving():
    amount = int(input("Enter the amount of saving: "))
    desc = input("Enter the description of the saving: ")
    store_data(amount, "Saving", desc)
    
def total():
    try:
        with open(JSON_FILE, "r") as json_file:
            data_list = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data_list = []

    balance = 0

    for data in data_list:
        if data["Type"] == "Income":
            balance += data["Amount"]
        elif data["Type"] == "Expense" or data["Type"] == "Saving":
            balance -= data["Amount"]

    print(f"Current Balance: ₹{balance}")


    
while True:
    option = int(input('''Enter your Option:
                        1. Expenses
                        2. Income
                        3. Saving
                        4. Total
                        5. Exit\n--> '''))


    if option == 1:
        expenses()
    elif option == 2:
        income()
    elif option == 3:
        saving()
    elif option == 4:
        total()
    elif option == 5:
        print("Thank you for using Personal Finance tracker!")
        exit()
    else:
        print("Invalid option")
        exit()

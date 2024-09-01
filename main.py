# write all the functions related to getting information from the user

from datetime import datetime

CATEGORIES = {'I':"Income", "E":"Expense"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime("%d-%m-%Y")
        # `.strftime`
        # Purpose: This method is used to format a datetime object into a string representation.
        # Functionality: It converts a datetime object into a string formatted according to a specified format.
    try:
        # `.strptime`
        # Purpose: This method is used to parse a string representation of a date and time into a datetime object.
        # Functionality: It converts a string formatted according to a specified format into a datetime object.
        valid_date = datetime.strptime(date_str, "%d-%m-%Y")
        return valid_date.strftime("%d-%m-%Y")
    
    # if user inputs "hello" like strings instead of proper date
    except ValueError:
        print("Invalid date format")
        print("Reenter date in dd-mm-yyyy format")
        return get_date(prompt , allow_default)


def get_amount():
    try:
        amount = float(input("Enter the amount : "))
        if amount<=0:
            raise ValueError("Amount must be > 0")
        return amount
    except ValueError as e:
        print(e)
        return get_amount
    
    
def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense) : ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    else:
        print("Invalid category. Please reenter the category : ")
        return get_category()
        

def get_description():
    return input("Enter description (optional) : ")


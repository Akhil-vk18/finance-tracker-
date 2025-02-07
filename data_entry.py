#all the functions associated with data entries are here 
from datetime import datetime

date_format="%d-%m-%Y"
categories ={'I' : "Income", 'E' : "Expense"}
def get_date(prompt,allow_default=False):
    #allow_default (bool): If True, allows the user to press Enter to use the current date as default.
    

    date_str=input(prompt)
    if allow_default and not date_str :
        return datetime.today().strftime(date_format)
    try:
         # Convert the string to a date object .validate date  
        valid_date=datetime.strptime(date_str,date_format)
        # Convert the date object back to a string in the desired format
        return valid_date.strftime(date_format)
    except ValueError:
        print("invalid date format.enter a valid date in the dd-mm-yyyy format ")
        return get_date(prompt,allow_default)#recursive function 

def get_amount():
    try:
        amount=float(input("Enter the amount : "))
        if amount<=0 :
            raise ValueError("amount should be non negative non zero value.")
        return amount
    except ValueError as e :
        print(e)
        return get_amount()
    
def get_category():
    category=input("Enter the category : ('I' for income and 'E' for expense .)").upper()
    if category in categories :
        return categories[category]
    print("Invalid category. Please enter a valid one")
    return get_category

def get_discription():
    return input("Enter the discription (optional) : ")
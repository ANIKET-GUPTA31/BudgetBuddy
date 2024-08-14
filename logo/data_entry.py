from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I":"Income", "E": "Expense"}


def get_date(prompt, allow_default=False):  # prompt :- is what we'er going to ask the user to input before they give us the date
    date_str = input(prompt) # input a date from user 
    if allow_default and not date_str:  # if user enter date not date str they input date from computer 
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format) # convert date string to
        return valid_date.strftime(date_format) # convert date to string
    except ValueError:
        print(" Invalid date format, Please enter the date in dd-mm-yyyy format ")
        return get_date(prompt, allow_default) # if date is not in correct format ask user again



def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative or non-zero values ")
        return amount
    
    except ValueError as e:
        print(e)
        return get_amount()



def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print ("INVALID CATEGORY. PLEASE ENTER 'I' FOR INCOME OR 'E' FOR EXPENSE. ")
    return get_category()




def get_description():
    return input("ENTER A DESCRIPTION (optional) ")


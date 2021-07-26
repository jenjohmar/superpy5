# Imports
from helpers import *

def buy(prod_name: str, buy_price: float, buy_date: str, exp_date: str, amount: int):
    #checks if format of dates is correct
    checkBuyDate = checkDate(buy_date)
    checkExpDate = checkDate(exp_date)
    # if format is correct executes code, if not error message
    if checkBuyDate == True and checkExpDate == True:
        # sell_date is converted to datetime object
        date = dt.datetime.strptime(buy_date, '%Y-%m-%d')
        # current date is stored as a datetime object
        today = dt.datetime.today()
        if date <= today:
            # code only executes if buy date are NOT in the future
            # sets number of lines in csv to 0
            number_of_lines = 0
            # creates bought.csv if not already there
            create_csv("bought.csv", header_bought)
            # opens and reads csv file
            with open('bought.csv', 'r') as csv_file:
                # increments number_of_lines with 1 for every line in csv file
                for line in csv_file:
                    number_of_lines += 1
            # stores id as total number of lines
            id = number_of_lines
            # creates dict of product passed in
            new_product_dict = {
                "bought_id": id,
                "product_name": prod_name,
                "buy_price": buy_price,
                "buy_date": buy_date,
                "exp_date": exp_date,
                }
            # writes product to bought.csv amount number of times
            for i in range(amount):
                write_to_bought(new_product_dict)
                # increments id with 1
                id += 1
                # replaces value of id with newest id value in dict
                new_product_dict["bought_id"] = id
                
            console.print(f"Product bought successfully!", style="bold green")
        else:
            console.print("Buy date cannot be in the future!", style="bold red")
    # error message if product passed in is not in string format
    else:
        console.print(f"Please enter the dates in correct format yyyy-mm-dd.", style="bold red")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Buy product(s).")
                
    parser.add_argument("prod_name", help="Enter product name in lowercase (i.e. 'orange').")
    parser.add_argument("buy_price", type=float, help="Enter product buy price (format 0.00).")
    parser.add_argument("buy_date", help="Enter product buy date (format: yyyy-mm-dd).")
    parser.add_argument("exp_date", help="Enter product expiration date (format: yyyy-mm-dd).")
    parser.add_argument("amount", type=int, help="Enter amount (number) of products to buy.")

    args = parser.parse_args()

    buy(prod_name=args.prod_name, buy_price=args.buy_price, buy_date=args.buy_date, exp_date=args.exp_date, amount=args.amount)
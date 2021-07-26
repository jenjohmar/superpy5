import argparse
from helpers import *

def sell(prod_name: str, sell_price: float, sell_date: str, amount: int):
    #checks if format of date is correct, if not error message
    checkSellDate = checkDate(sell_date)
    # if format date is correct executes code 
    if checkSellDate == True:
        # sell_date is converted to datetime object
        date = dt.datetime.strptime(sell_date, '%Y-%m-%d')
        # current date is stored as a datetime object
        today = dt.datetime.today()
        # code only executes if both dates are NOT in the future
        if date <= today:
            create_csv("sold.csv", header_sold)
            # sets number_of_lines in csv file to 0 
            number_of_lines = 0
            # opens and reads csv file
            with open('sold.csv', 'r') as csv_file:
                for line in csv_file:
                    # looks at current line count adss 1 to number_of_lines for each line,
                    # skips header
                    if "sold_id" in line:
                        continue
                    # increments number_of_lines with 1 for each line in csv file
                    number_of_lines += 1
            # id is the same as number of lines counted
            id = number_of_lines
            # returns total inventory of today  
            inventory = check_inventory(sell_date, prod_name)
            # list to hold only those items from inventory that are == to passed in product
            items_to_be_sold = []
            # creates new dict from data passed in, adds sold_id + stand-in value for bought_id 
            new_product_dict = {
                "sold_id": id,
                "bought_id": 0,
                "product_name": prod_name,
                "sell_price": sell_price,
                "sell_date": sell_date,
                }
            # all items with the same name as product passed in are added to list
            for item in inventory:
                if prod_name in item:
                    items_to_be_sold.append(item)
            # checks if items to be sold >= amount given, if true executes code
            if len(items_to_be_sold) >= amount:
                # reduces items in items_to_be_sold to amount given
                items_to_be_sold = items_to_be_sold[:amount]
                # writes to sold amount times
                for product in items_to_be_sold:
                    # stores bought_id
                    bought_id = product[0]
                    # increments sold id with 1
                    id += 1
                    # replaces sold_id with new sold_id
                    new_product_dict["sold_id"] = id
                    # replaces bought_id with new bought_id
                    new_product_dict["bought_id"] = bought_id
                    # writes dict to sold
                    write_to_sold(new_product_dict) 
                console.print(f"Product {prod_name} sold succesfully!", style="bold green")
            # error message if there are not enough items in inventory to sell on current day
            else: 
                console.print(f"Amount exceeds product count in inventory! You can sell {len(items_to_be_sold)} of {prod_name}.")
        # error message if sell date is in the future
        else:
            console.print(f"ERROR: Sell date cannot be in the future!", style="bold red")
    # error message if sell date is entered in the wrong format
    else:
        console.print("Please enter the date in correct format yyyy-mm-dd.", style="bold red")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sell product(s).")
                
    parser.add_argument("prod_name", help="Enter product name in lowercase (i.e. 'orange').")
    parser.add_argument("sell_price", type=float, help="Enter product sell price (format: 0.00).")
    parser.add_argument("sell_date", help="Enter product sell date (format: yyyy-mm-dd).")
    parser.add_argument("amount", type=int, help="Enter amount (number) to sell.")

    args = parser.parse_args()

    sell(prod_name=args.prod_name, sell_price=args.sell_price, sell_date=args.sell_date, amount=args.amount)

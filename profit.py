from helpers import *

def profit(start_date: str, end_date: str, product: str):
    #checks if format of dates are correct
    checkStartDate = checkDate(start_date)
    checkEndDate = checkDate(end_date)
    # if both formats are correct executes code, if not error message
    if checkStartDate == True and checkEndDate == True:
        # start_date is converted to datetime object
        date1 = dt.datetime.strptime(start_date, '%Y-%m-%d')
        # end_date is converted to datetime object
        date2 = dt.datetime.strptime(end_date, '%Y-%m-%d')
        # current date is stored as a datetime object
        today = dt.datetime.today()
        # code only executes if both dates are NOT in the future
        if date1 <= today and date2 <= today:
            # stores all bought products until and including given end_date in a list
            bought_list = get_bought(end_date)
            # stores all sold products until and including given end_date in a list
            sold_list   = get_sold(end_date)
            # if user wants profit report for all products by passing in "all", this code gets executed                        
            if product == "all" and len(bought_list) > 0:
                # sum of total bought and sold is set to 0
                total_bought = 0
                total_sold   = 0
                # adds buy price for each product bought in given timeframe to sum total_bought                
                for bought_product in bought_list:
                    #buy_date = bought_product[3]
                    buy_date = dt.datetime.strptime(bought_product[3], '%Y-%m-%d')
                    if buy_date >= date1 and buy_date <= date2:
                        buy_price = float(bought_product[2])
                        total_bought += buy_price
                # adds sell price for each product sold in given timeframe to sum total_sold
                for sold_product in sold_list:
                    sell_date = sold_product[4]
                    sell_date = dt.datetime.strptime(sell_date, '%Y-%m-%d')
                    if sell_date >= date1 and sell_date <= date2:
                        sell_price = float(sold_product[3])
                        total_sold += sell_price
                # calculates profit                                
                profit = total_sold - total_bought
                # if profit is over 0, display profit in green
                if profit > 0:
                    console.print(f"The total profit from {start_date} until {end_date} for {product} is [green]{profit:.2f}[/]")
                # if profit is 0, display profit in grey
                elif profit == 0:
                    console.print(f"The total profit from {start_date} until {end_date} for {product} is [grey]{profit:.2f}[/]")
                # if profit is a negative number, display profit in red
                else:
                    console.print(f"The total loss from {start_date} until {end_date} for {product} is [red]{profit:.2f}[/]")                                            
            elif len(bought_list) == 0:
                console.print(f"Nothing in inventory between {start_date} and {end_date}. Profit/loss cannot be computed.")
            # if user wants profit report for specific product i.e. "orange", this code gets executed    
            elif type(product) == str:
                # sum of total bought and sold is set to 0
                total_bought = 0
                total_sold   = 0
                # filters specified product from bought_list
                for list_item in bought_list:
                    if product in list_item:
                        # adds buy price for each product bought in given timeframe to sum total_bought
                        for bought_product in bought_list:
                            buy_date = bought_product[3]
                            buy_date = dt.datetime.strptime(buy_date, '%Y-%m-%d')
                            if product in bought_product and buy_date >= date1 and buy_date <= date2:
                                buy_price = float(bought_product[2])
                                total_bought += buy_price
                        # adds sell price for each product sold in given timeframe to sum total_sold
                        for sold_product in sold_list:
                            sell_date = sold_product[4]
                            sell_date = dt.datetime.strptime(sell_date, '%Y-%m-%d')
                            if product in sold_product and sell_date >= date1 and sell_date <= date2:
                                sell_price = float(sold_product[3])
                                total_sold += sell_price
                        # calculates profit                                
                        profit = total_sold - total_bought
                        # if profit is over 0, display profit in green
                        if profit > 0:
                            console.print(f"The total profit from {start_date} until {end_date} for {product} is [green]{profit:.2f}[/]")
                        elif profit == 0:
                            console.print(f"The total profit from {start_date} until {end_date} for {product} is [grey]{profit:.2f}[/]")
                        # if profit is a negative number, display profit in red
                        else:
                            console.print(f"The total loss from {start_date} until {end_date} for {product} is [red]{profit:.2f}[/]")
                        return     
                # error message if a string passed in as product is not in inventory        
                console.print(f"Product [bold underline]not[/] in inventory between {start_date} and {end_date}. Profit/loss cannot be computed.")    
            # error message if value passed in as product is not a string     
            else:
                console.print("Please enter a valid product name (i.e. 'orange') or 'all'.", style="bold red")
        # error message if date(s) passed in are in the future
        else:
            console.print(f"ERROR: Dates cannot be in the future!", style="bold red")
    # error message of dates passed in do not have the right format
    else:
        console.print(f"Please enter the [underline]dates[/] in correct format yyyy-mm-dd.", style="bold red")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Report total or product profit for specified timeframe.")
                
    parser.add_argument("start_date", help="Enter start date for timeframe (format: yyyy-mm-dd).")
    parser.add_argument("end_date", help="Enter end date for timeframe (format: yyyy-mm-dd).")
    parser.add_argument("product", help="Enter product in lowercase (i.e. 'orange') or 'all' for the profit report.")

    args = parser.parse_args()

    profit(start_date=args.start_date, end_date=args.end_date, product=args.product)
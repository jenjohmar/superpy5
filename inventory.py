from helpers import *

def get_inventory(date: str, product: str):
    #checks if format of date is correct
    checkInvDate = checkDate(date)
    # if date format is correct executes, if not error message
    if checkInvDate == True:
        # stores all products bought to bought_list until and incl. date
        bought_list = get_bought(date)
        # stores all products sold to sold_list until and incl. date
        sold_list = get_sold(date)
        # stores all products expired to exp_list until and incl. date
        exp_list = get_expired(date)
        # for each sold product in sold list 
        for sold_product in sold_list:
            # look at each bought product in bought list
            for bought_product in bought_list:
                # if product id matches, remove product from bought list
                if sold_product[1] == bought_product[0]:
                    bought_list.remove(bought_product)
        # for each expired product in expired list
        for exp_product in exp_list:
            # look at each bought product in bought list
            for bought_product in bought_list:
                # if product id matches remove product from bought list
                if exp_product[0] == bought_product[0]:
                    bought_list.remove(exp_product)
        # stores inventory as a dict of products and their amounts 
        inv_list = count_inventory(bought_list)
        
        # if there are products in inventory, executes code, else error message
        if len(bought_list) > 0:
            # if user want to know total inventory
            if product == "all":
                # prints all products in inventory with their amounts
                print_dict(inv_list)
            # if user wants to know inventory for specific product
            elif type(product) == str:
                # if given product is in inventory
                if product in inv_list:
                    # prints product with amount
                    print_dict({product: inv_list[product]})
                # if given product is not in inventory
                else:
                    # print error message
                    console.print("Product [bold underline]not[/] in inventory.")        
            # if format of product given is not a string
            else:
                # print error message
                console.print("Format not correct.", style="bold red")
        # if bought_list is empty    
        else:
            # print error message
            print("Nothing in inventory.")
    # if date not entered in correct format
    else:
        # print error message
        console.print(f"Please enter the date in correct format yyyy-mm-dd.", style="bold red")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Report inventory.")
                
    parser.add_argument("date", help="Enter date for the inventory on that date (format yyyy-mm-dd).")
    parser.add_argument("product", help="Enter product name (i.e. 'orange') in lowercase or 'all'.")


    args = parser.parse_args()

    get_inventory(date=args.date, product=args.product)




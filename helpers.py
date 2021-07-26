# Imports
import argparse
import csv
import datetime as dt
from datetime import date, time
import os
import operator
from types import new_class
from rich.console import Console
from rich.traceback import install
install()

console = Console()

# stores current date as datetime object
current_date = dt.date.today()
# converts current date to string
current_date = current_date.strftime("%Y-%m-%d")

# column headers for .csv files
header_bought       = ["bought_id", "product_name", "buy_price", "buy_date", "exp_date"]
header_sold         = ["sold_id", "bought_id",  "product_name", "sell_price", "sell_date"]

# creates needed csv database if it doesn't yet exist
def create_csv(name_csv, header):
    current_dir = os.getcwd() + ("/" + name_csv)
    if not os.path.exists(current_dir):
        with open(name_csv, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()

# writes the data from the dictionary passed in through the buy function, to bought.csv 
def write_to_bought(bought_dict): # new_product_dict from buy function gets passed in
    create_csv("bought.csv", header_bought)
    with open('bought.csv', 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header_bought)
        csv_writer.writerow(bought_dict)

# writes the data from the dictionary passed in through the sell function, to sold.csv
def write_to_sold(sold_dict): # new_product_dict from sell function gets passed in
    create_csv("sold.csv", header_sold)
    with open('sold.csv', 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header_sold)
        csv_writer.writerow(sold_dict)

# writes the data from the dictionary passed in through the sell function, to sold.csv
def write_to_sold(sold_dict): # new_product_dict from sell function gets passed in
    create_csv("sold.csv", header_sold)
    with open('sold.csv', 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header_sold)
        csv_writer.writerow(sold_dict)

def get_bought(date):
    # converts date to date object
    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    bought_list = []

    # in case there is not yet a bought.csv it gets created
    create_csv("bought.csv", header_bought)
    # opens and reads csv file
    with open('bought.csv', 'r') as csv_file:
        # looks at each line in csv file
        for line in csv_file:
            # skips the header
            if "bought_id" in line:
                continue
            # removes the /n from line
            line = line[:-1]
            # stores the buy date of the product
            buy_date = line.split(",")[3]
            # converts the buy date to date object
            buy_date = dt.datetime.strptime(buy_date, "%Y-%m-%d").date()
            # appends product line to bought_list if buy date <= date 
            if buy_date <= date:
                bought_list.append(line.split(","))
                 
    return bought_list 

def get_sold(date):
    # converts date to date object
    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    sold_list = []
    
    # in case there is not yet a sold.csv it gets created
    create_csv("sold.csv", header_sold)
    # opens and reads csv file
    with open('sold.csv', 'r') as csv_file:
        # looks at each line in csv file
        for line in csv_file:
            # skips the header
            if "sold_id" in line:
                continue
            # removes the /n from line
            line = line[:-1]
            # stores the sell date of the product
            sell_date = line.split(",")[4]
            # converts the sell date to date object
            sell_date2 = dt.datetime.strptime(sell_date, "%Y-%m-%d").date()
            # appends product line to sold_list if sell date <= date
            if sell_date2 <= date:
                sold_list.append(line.split(","))

    return sold_list

# gets used in inventory
def get_expired(date):
    # converts date to date object
    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    exp_list = []
    # opens and reads csv file
    with open("bought.csv", "r") as csv_file:
        # looks at each line in csv file
        for line in csv_file:
            # skips the header
            if "bought_id" in line:
                continue
            # removes the /n from line
            line = line[:-1]
            # stores the expiration date of the product
            exp_date = line.split(",")[4]
            # converts the expiration date to date object
            exp_date = dt.datetime.strptime(exp_date, "%Y-%m-%d").date()
            # appends product line to exp_list if expiration date < date
            if exp_date < date:
                exp_list.append(line.split(","))
   
    return exp_list

# 1. "list" = list of the first elements of lists in bought_list passed in via get_inventory()
# 2. list items from list are stored in new_dict with their amount
# 3. returns new_dict
def count_inventory(list1):
    list = [item[1] for item in list1]
    new_dict = {}

    for product in list:
        if product not in new_dict:
            count = list.count(product)
            new_dict[product] = count
    
    return new_dict

# 1. prints header
# 2. prints product name and amount
def print_dict(dict):
    print("Product, Amount")
    for product, count in dict.items():
        print(f"{product}, {count}")

#creates txt file in turnover function
def create_txt(file):
    current_dir = os.getcwd() + ("/" + file)
    if not os.path.exists(current_dir):
        txt_file = open(file, "w+")

# checks inventory in sell function to see if product can be sold
# argument product is not used in this function but will be passed in when the function is called in the sell function
def check_inventory(date, product): 
    # stores all bought products until and incl. date
    bought_list = get_bought(date)
    # stores all sold products until and incl. date
    sold_list = get_sold(date)
    # stores all expired products until and incl. date
    exp_list = get_expired(date)
    
    # if there are no sold products
    if len(sold_list) == 0:
        # for each expired product in exp_list
        for exp_product in exp_list:
            # look at each product in bought_list
            for bought_product in bought_list:
                # if product id matches, remove this product from bought_list
                if exp_product[0] == bought_product[0]:
                    bought_list.remove(exp_product)
        return bought_list
    # for each sold product in sold_list
    for sold_product in sold_list:
        # look at each bought product in bought_list
        for bought_product in bought_list:
            # if product id matches, remove product from bought_list
            if sold_product[1] == bought_product[0]:
                bought_list.remove(bought_product)
    # for each expired product in exp_list
    for exp_product in exp_list:
        # look at each bought product in bought_list
        for bought_product in bought_list:
            # if product id matches, remove product from bought_list
            if exp_product[0] == bought_product[0]:
                bought_list.remove(exp_product)
    # the bought_list is now the inventory list
    return bought_list

# check to see if dates are passed in in the correct format
def checkDate(date):
    count_num = 0
    count_dash = 0

    for i in date:
        if i.isnumeric():
            count_num += 1
        if i == "-":
            count_dash += 1
    if (count_num < 6 or count_num > 8) or count_dash != 2:
        return False

    else:
        return True
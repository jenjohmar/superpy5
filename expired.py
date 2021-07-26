from helpers import *

def get_exp_notsold(start_date, end_date, product):
    exp_list = get_expired(end_date)
    sold_list = get_sold(end_date)
    new_exp_list = []
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
       
    if product == "all":
        for exp_prod in exp_list:
            found = False
            exp_date = dt.datetime.strptime(exp_prod[4], '%Y-%m-%d').date()
            
            for sold_prod in sold_list:
                if exp_prod[0] == sold_prod[1]:
                    found = True
            if found == False:
                if exp_date >= start_date and exp_date <= end_date:
                    new_exp_list.append(exp_prod)
        
        if len(new_exp_list) > 0:    
            with open("expired.csv", "w", newline='') as csv_file:
                message = f"ALL EXPIRED PRODUCTS FROM {start_date} TO {end_date}."
                writer = csv.writer(csv_file)
                writer.writerow([message])
                writer.writerow(header_bought)
                writer.writerows(new_exp_list)
                    
            console.print(f"All expired products from {start_date} to {end_date} have been exported to expired.csv.", style="green")    
        else:
            console.print(f"No expired products in given timeframe.")
    
    elif type(product) == str:
        for exp_prod in exp_list:
            found = False
            exp_date = dt.datetime.strptime(exp_prod[4], '%Y-%m-%d').date()
            
            for sold_prod in sold_list:
                if exp_prod[0] == sold_prod[1]:
                    found = True
            if found == False:
                if exp_date >= start_date and exp_date <= end_date and product in exp_prod:
                    new_exp_list.append(exp_prod)
        
        if len(new_exp_list) > 0:    
            with open("expired.csv", "w", newline='') as csv_file:
                message = f"EXPIRED ITEMS FOR PRODUCT: {product} FROM {start_date} TO {end_date}."
                writer = csv.writer(csv_file)
                writer.writerow([message])
                writer.writerow(header_bought)
                writer.writerows(new_exp_list)
                    
            console.print(f"Expired items for product: {product} from {start_date} to {end_date} have been exported to expired.csv.", style="green")    
        else:
            console.print(f"No expired items for product: {product} in given timeframe.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export expired products to .csv.")
                
    parser.add_argument("start_date", help="Enter start date for timeframe (format yyyy-mm-dd).")
    parser.add_argument("end_date", help="Enter end date for timeframe (format yyyy-mm-dd).")
    parser.add_argument("product", help="Enter product name (i.e. 'orange') in lowercase or 'all'.")


    args = parser.parse_args()

    get_exp_notsold(start_date=args.start_date, end_date=args.end_date, product=args.product)



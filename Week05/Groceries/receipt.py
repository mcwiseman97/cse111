import csv
import datetime as dt
def main():

        current_time = dt.datetime.now()
        formatted_time = current_time.strftime("%a %b %d %H:%M:%S %Y")
        running_total = 0
        prod_file = "CSE111/W05/Groceries/products.csv"
        req_file = "CSE111/W05/Groceries/request.csv"
        product_dict = read_dictionary(prod_file, 0)
        
        print("\nInkom Imporium")

        with open(req_file) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            try:
                for row in reader:
                    product_number = row[0]
                    quantity = int(row[1])
                    product_row = product_dict[product_number]
                    name = product_row[1]
                    price = float(product_row[2])
                    print(f"{name}: {quantity} @ ${price:.2f}")
                    total = quantity * price
                    running_total += total
            except:
                print("A requested item is not a real product")
            # Use running total from for loop to finish calculating total cost.        
            print(f"Subtotal: ${running_total:.2f}")
            tax = running_total * .06
            print(f"Sales Tax: ${tax:.2f}")
            running_total += tax
            print(f"Total: ${running_total:.2f}")
            print("Thank you for shopping at Inkom Imporium!")
            print(formatted_time)
            print()


def read_dictionary(filename, key_index):
    result = {}
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            result[row[key_index]] = row
    return result

if __name__ == "__main__":
    main()

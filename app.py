from models import(Base, session, Product, engine)

import datetime
import csv


def menu():
    while True:
        print('''
              \nPRODUCT'S INVENTORY
              \ra - Add a new product to the database
              \rb - Make a backup of the entire inventory
              \rv - View a single product's inventory
              ''')
        choice = input('\nWhat would you like to do?  ').lower()
        if choice in ['a', 'b', 'v']:
            return choice
        else:
            input('''
                  \rPlease only choose one of the options (a / b / v).
                  \rPlease enter to try again.''')


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''===DATE ERROR===
              \rThe only format accept is (Ex: MM/DD/YYYY).
              \rPress enter to try again.''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        split_price = price_str.split('$')
        return_price = int(float(split_price[1]) * 100)
    except ValueError:
        input('''
            \n****** PRICE ERROR ******
            \rThe price should be a number without a currency symbol.
            \rExample: 6.99
            \rPress enter to try again.
            \r************************''')
        return
    else:
        return return_price


def clean_quantity(quantity_str):
    try:
        clean_quantity = int(quantity_str)
    except ValueError:
        input('''===QUANTITY ERROR===
              \rThe only format accept is a number (Ex: 22).
              \rPress enter to try again.''')
        return
    else:
        return clean_quantity

def add_csv_to_db():
    with open('inventory.csv') as file:
        data = csv.reader(file)
        next(data) # jump the title table
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = clean_quantity(row[2])
                date = clean_date(row[3])
                new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date)
                session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'a':
            
            name = input('Product name: ')
            
            price_error = True
            while price_error:
                price = input('Price name (Ex: 33.19): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
    
            quantity = int(input('Product quantity: '))
            
            date_error = True
            while date_error:
                date = input('Date (Ex: MM/DD/YYYY): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            
            new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date)
            session.add(new_product)
            session.commit()
            
        elif choice == 'b':
            pass
        elif choice == 'v':
            pass
        else:
            print('Goodbye! Thank you for used the app.')
            app_running = False



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv_to_db()
    
    for product in session.query(Product):
        print(Product)
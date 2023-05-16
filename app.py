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
              \rq - Quit
              ''')
        choice = input('\nWhat would you like to do?  ').lower()
        if choice in ['a', 'b', 'v', 'q']:
            return choice
        else:
            input('''
                  \rPlease only choose one of the options (a / b / v).
                  \rPlease enter to try again.''')


def clean_id(id_str, option):
    try:
        id_integer = int(id_str)
        if id_integer in option:
            return id_integer
        else:
            input(f'''===ID ERROR===
                  \rThe number need to be between {option[0]} and {option[-1]}.
                  \rPress enter to try again.
                  \r======================''')
            return False
    except ValueError:
        input('''===ID ERROR===
              \rThe only format accept is a number (Ex: 22).
              \rPress enter to try again.
              \r======================''')
        return False


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        default_date = datetime.date(year, month, day)
    except ValueError:
        input('''
              \r====DATE ERROR===
              \rThe only format accept is (Ex: MM/DD/YYYY).
              \rPress enter to try again.
              ===================''')
        return
    else:
        return default_date


def clean_price(price_str):
    try:
        if '$' not in price_str:
            raise ValueError
        split_price = price_str.split('$')
        price_integer = int(float(split_price[1]) * 100)
    except ValueError:
        input('''
            \r==== PRICE ERROR ===
            \rThe price should be a currency symbol followed by the number.
            \rExample: $6.99
            \rPress enter to try again.
            \r===================''')
        return
    else:
        return price_integer


def clean_quantity(quantity_str):
    try:
        quantity_integer = int(quantity_str)
    except ValueError:
        input('''
              \r=====QUANTITY ERROR======
              \rThe only format accept is a number (Ex: 22).
              \rPress enter to try again.
              \r======================''')
        return
    else:
        return quantity_integer


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


def add_product():
    name = input('Product name: ')
    
    price_error = True
    while price_error:
        price = input('Product price (Ex: $33.19): ')
        price = clean_price(price)
        if type(price) == int:
            price_error = False
            
    quantity_error = True
    while quantity_error:
        quantity = input('Product quantity: ')
        quantity = clean_quantity(quantity)
        if type(quantity) == int:
            quantity_error = False     
               
    date = datetime.date.today()
    
    new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date)
    
    # check
    product_in_db = session.query(Product).filter(Product.product_name==name).one_or_none()
    
    # if product not exist
    if product_in_db == None:
        session.add(new_product)
        session.commit()
        print('\nProduct added!')
    
    # if product exist
    else:
        product_in_db.product_quantity = new_product.product_quantity
        product_in_db.product_price = new_product.product_price
        product_in_db.date_updated = new_product.date_updated
        session.commit()
        print('\nProduct updated!')
       

def view_database():
    ids_available = []
    for product in session.query(Product):
        ids_available.append(product.product_id)
    
    id_error = True
    while id_error:
        choice_id = input('\nType the product id (Ex: 4): ')
        choice_id = clean_id(choice_id, ids_available)
        if choice_id == False:
            id_error = True
        else:
            id_error = False
    
    # With the choice_id, we can find the product in the database and display it
    for product in session.query(Product):
        if product.product_id == choice_id:
            print(f'''
                \rProduct Name: {product.product_name}
                \rPrice: ${product.product_price}
                \rQuantity: {product.product_quantity}
                \rDate Updated: {product.date_updated}
                ''')


# Create a function to make a backup of the entire inventory.db file in a new file called backup_csv.
def make_backup():
    with open('backup.csv', 'w') as file:
        header = ['Product Name', 'Product Price', 'Product Quantity', 'Date Updated']
        data_backup = csv.writer(file)
        data_backup.writerow(header)
        for product in session.query(Product):
            file.write(f'{product.product_name}, {product.product_price}, {product.product_quantity}, {product.date_updated}\n')
    print('\nBackup complete!')


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'a':
            add_product()
            input('\nPress enter to return to the main menu.')
            
        elif choice == 'b':
            make_backup()
            input('\nPress enter to return to the main menu.')
        
        elif choice == 'v':
            view_database()
            input('\nPress enter to return to the main menu.')

        else:
            print('\nGoodbye! Thank you for used the app.')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv_to_db()
    app()
    
    for product in session.query(Product):
        print(Product)
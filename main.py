
import sqlite3

db = sqlite3.connect('Kompiuteriu_parduotuve.db')

cursor = db.cursor()

#cursor.execute(""" CREATE TABLE products(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price INTEGER, quantity INTEGER)""")
#cursor.execute(""" CREATE TABLE sellers(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, selling INTEGER)""")
#cursor.execute(""" CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, seller_id INTEGER, quantity INTEGER, FOREIGN KEY (product_id) REFERENCES products (id), FOREIGN KEY (seller_id) REFERENCES sellers (id))""")

def add_product():
    name = input("Enter the product name:")
    price = float(input("Enter the price fo the product:"))
    quantity = input("Enter the quantity of the product:")
    cursor.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
    db.commit()
    print("Product successfully added!")

def add_seller():
    name = input("Enter the seller name:")
    selling = input("Enter selling of the seller:")
    cursor.execute('INSERT INTO sellers (name, selling) VALUES (?, ?)', (name, selling))
    db.commit()
    print("Seller successfully added!")

def make_sale():
    product_name = input("Enter the product name: ")
    quantity = int(input("Enter the quantity to sell: "))
    seller_name = input("Enter the seller name:")

    cursor.execute('SELECT id, quantity FROM products WHERE name=?', (product_name,))
    product = cursor.fetchone()
    if product is None:
        print("Product not found.")
        return
    product_id, available_quantity = product

    cursor.execute('SELECT id FROM sellers WHERE name=?', (seller_name,))
    seller = cursor.fetchone()
    if seller is None:
        print("Seller not fount.")
        return
    seller_id = seller[0]

    if quantity > available_quantity:
        print("Not enough quantity available.")
        return

    cursor.execute('INSERT INTO sales (product_id, seller_id, quantity) VALUES (?, ?,?)', (product_id, seller_id, quantity))
    db.commit()
    print("Sale successfully recorded.")

    cursor.execute('UPDATE sellers SET selling = selling + 1 WHERE id = ?', (seller_id,))
    db.commit()

    cursor.execute('UPDATE products SET quantity = quantity - ? WHERE id = ?', (quantity, product_id))
    db.commit()

def show_products():
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Price: {row[2]}, Quantity: {row[3]}")
    else:
        print("There are no products available.")

def show_sellers():
    cursor.execute('SELECT * FROM sellers')
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Selling: {row[2]}")
    else:
        print("There are no sellers available.")

def show_sales():
    cursor.execute('SELECT sales.id, products.name, sellers.name, sales.quantity FROM sales '
                   'INNER JOIN products ON sales.product_id = products.id '
                   'INNER JOIN sellers ON sales.seller_id = sellers.id')
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"Sale ID: {row[0]}, Product: {row[1]}, Seller: {row[2]}, Quantity: {row[3]}")
    else:
        print("The are no sales available.")

def update_product():
    product_id = input("Enter the ID of the product to update: ")
    new_price = float(input("Enter the new price of the product: "))
    new_quantity = int(input("Enter the new quantity of the product: "))

    cursor.execute('UPDATE products SET price =?, quantity = ? WHERE id = ?', (new_price, new_quantity, product_id))
    db.commit()
    print("Product successfully updated!")

def update_seller():
    seller_id = input("Enter the ID of the seller to update: ")
    new_selling = input("Enter the new selling of the seller: ")

    cursor.execute('UPDATE sellers SET selling = ? WHERE id = ?', (new_selling, seller_id))
    db.commit()
    print("Seller successfully update!")

def delete_product():
    product_id = input("Enter the ID of the product to delete: ")
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    db.commit()
    print("Product successfully deleted!")

def delete_seller():
    seller_id = input("Enter the ID of the seller to delete: ")
    cursor.execute('DELETE FROM sellers WHERE id = ?', (seller_id,))
    db.commit()
    print("Seller successfully deleted!")


while True:
    print("\n=== MENU ===")
    print("1. Add")
    print("2. Show")
    print("3. Make Sale")
    print("4. Update")
    print("5. Delete")
    print("0. Exit")

    choice = input("Enter the number: ")
    if choice == "1":
        print("1. Add product")
        print("2. Add seller")
        sub_choice = input("Enter the number: ")
        if sub_choice == "1":
            add_product()
        elif sub_choice == "2":
            add_seller()

    elif choice == "2":
        print("1. Show products")
        print("2. Show seller")
        print("3. Show sales")
        sub_choice = input("Enter the number: ")
        if sub_choice == "1":
            show_products()
        elif sub_choice == "2":
            show_sellers()
        elif sub_choice == "3":
            show_sales()

    elif choice == "3":
        make_sale()

    elif choice == "4":
        print("1. Update product")
        print("2. Update seller")
        sub_choice = input("Enter the number: ")
        if sub_choice == "1":
            update_product()
        elif sub_choice == "2":
            update_seller()

    elif choice == "5":
        print("1. Delete product")
        print("2. Delete seller")
        sub_choice = input("Enter the number: ")
        if sub_choice == "1":
            delete_product()
        elif sub_choice == "2":
            delete_seller()

    elif choice == "0":
        break
    else:
        print("Incorrect choice. Try again.")


db.close()

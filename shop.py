import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# Create Products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock_quantity INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("Database for MAMA MORAAS' SHOP created successfully!")
def add_product(name, price, stock_quantity):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Products (name, price, stock_quantity) VALUES (?, ?, ?)",
                   (name, price, stock_quantity))
    conn.commit()
    conn.close()
    print(f"Product '{name}' added successfully to MAMA MORAAS' SHOP!")
add_product("weighing Sugar", 160, 20,)
add_product("Cooking Oil", 260, 80)
import sqlite3
from datetime import datetime

def record_purchase(product_id, supplier, quantity, cost):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    # Insert purchase record into Purchases table
    cursor.execute("""
    INSERT INTO Purchases (product_id, supplier, quantity, cost, purchase_date)
    VALUES (?, ?, ?, ?, ?)
    """, (product_id, supplier, quantity, cost, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # Update stock in Products table
    cursor.execute("""
    UPDATE Products
    SET stock_quantity = stock_quantity + ?
    WHERE product_id = ?
    """, (quantity, product_id))

    conn.commit()
    conn.close()
    print(f"Purchase recorded: {quantity} units added for product ID {product_id}.")
("weighing Sugar", "Takbir", 20, 6080,)  
import sqlite3
from datetime import datetime

def record_sale(product_id, quantity):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    # Get product price
    cursor.execute("SELECT price, stock_quantity FROM Products WHERE product_id = ?", (product_id,))
    result = cursor.fetchone()

    if result is None:
        print(f"Error: Product ID {product_id} not found.")
        conn.close()
        return

    price, current_stock = result

    # Check if enough stock is available
    if quantity > current_stock:
        print(f"Error: Not enough stock. Current stock = {current_stock}")
        conn.close()
        return

    total_amount = price * quantity

    # Insert sale record into Sales table
    cursor.execute("""
    INSERT INTO Sales (product_id, quantity, sale_date, total_amount)
    VALUES (?, ?, ?, ?)
    """, (product_id, quantity, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_amount))

    # Update stock in Products table
    cursor.execute("""
    UPDATE Products
    SET stock_quantity = stock_quantity - ?
    WHERE product_id = ?
    """, (quantity, product_id))

    conn.commit()
    conn.close()
    print(f"Sale recorded: {quantity} units sold for product ID {product_id}. Total = {total_amount}")
import sqlite3

def generate_report():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    print("\n===== REPORT: MAMA MORAAS' SHOP =====")

    # Total Purchases
    cursor.execute("SELECT SUM(cost) FROM Purchases")
    total_purchases = cursor.fetchone()[0]
    if total_purchases is None:
        total_purchases = 0
    print(f"Total Purchases (Goods Bought): {total_purchases}")

    # Total Sales
    cursor.execute("SELECT SUM(total_amount) FROM Sales")
    total_sales = cursor.fetchone()[0]
    if total_sales is None:
        total_sales = 0
    print(f"Total Sales: {total_sales}")

    # Profit (Sales - Purchases)
    profit = total_sales - total_purchases
    print(f"Profit: {profit}")

    # Current Stock
    print("\nCurrent Stock Levels:")
    cursor.execute("SELECT product_id, name, price, stock_quantity FROM Products")
    products = cursor.fetchall()
    for product in products:
        product_id, name, price, stock_quantity = product
        print(f"ID {product_id} | {name} | Price: {price} | Stock: {stock_quantity}")

    conn.close()
    print("===== END OF REPORT =====\n")
def main_menu():
    while True:
        print("\n===== MAMA MORAAS' SHOP SYSTEM =====")
        print("1. Add Product")
        print("2. Record Purchase")
        print("3. Record Sale")
        print("4. Generate Report")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            stock = int(input("Enter initial stock quantity: "))
            add_product(name, price, stock)

        elif choice == "2":
            product_id = int(input("Enter product ID: "))
            supplier = input("Enter supplier name: ")
            quantity = int(input("Enter quantity purchased: "))
            cost = float(input("Enter total cost: "))
            record_purchase(product_id, supplier, quantity, cost)

        elif choice == "3":
            product_id = int(input("Enter product ID: "))
            quantity = int(input("Enter quantity sold: "))
            record_sale(product_id, quantity)

        elif choice == "4":
            generate_report()

        elif choice == "5":
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
           
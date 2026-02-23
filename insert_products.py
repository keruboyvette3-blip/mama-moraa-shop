import sqlite3

# Connect to the database
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# List of products: (name, quantity, price)
products = [
    ("Sugar", 10, 120),
    ("Flour", 20, 80),
    ("Rice", 15, 150),
    ("Cooking Oil", 8, 250),
    ("Salt", 30, 25),
    ("Bread 600g", 12, 100),
    ("Bread 400g", 8, 65)
]

# Insert products into the table
cursor.executemany(
    "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
    products
)

conn.commit()
conn.close()

print("Products inserted successfully!")

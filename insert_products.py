import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# Insert sample products
products = [
    ("Bread 600g", 100),
    ("Bread 400g", 65)
]

cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", products)

conn.commit()
conn.close()

print("Sample products inserted successfully!")

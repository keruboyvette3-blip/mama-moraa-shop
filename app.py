from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Products
@app.route("/products", methods=["GET", "POST"])
def products():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    return render_template("products.html", products=products)

# Purchases
@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    if request.method == "POST":
        product_id = request.form["product_id"]
        quantity = request.form["quantity"]
        cursor.execute("INSERT INTO purchases (product_id, quantity) VALUES (?, ?)", (product_id, quantity))
        conn.commit()

    cursor.execute("SELECT * FROM purchases")
    purchases = cursor.fetchall()
    conn.close()

    return render_template("purchases.html", purchases=purchases)

# Sales
@app.route("/sales", methods=["GET", "POST"])
def sales():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    if request.method == "POST":
        product_id = request.form["product_id"]
        quantity = int(request.form["quantity"])

        # Get product price
        cursor.execute("SELECT price FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if product:
            price = product[0]
            total = price * quantity

            # Save sale with total (date auto-added by schema)
            cursor.execute("INSERT INTO sales (product_id, quantity) VALUES (?, ?)", (product_id, quantity))
            conn.commit()

            return f"Sale recorded! Total = {total} Ksh"

    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()
    conn.close()

    return render_template("sales.html", sales=sales)

# Reports
@app.route("/reports")
def reports():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    # Products
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    # Purchases
    cursor.execute("SELECT * FROM purchases")
    purchases = cursor.fetchall()

    # Sales
    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()

    # --- Grand Total Revenue ---
    cursor.execute("""
        SELECT SUM(p.price * s.quantity)
        FROM sales s
        JOIN products p ON s.product_id = p.id
    """)
    total_revenue = cursor.fetchone()[0] or 0

    # --- Today's Revenue ---
    cursor.execute("""
        SELECT SUM(p.price * s.quantity)
        FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE DATE(s.date) = DATE('now')
    """)
    today_revenue = cursor.fetchone()[0] or 0

    conn.close()

    return render_template(
        "reports.html",
        products=products,
        purchases=purchases,
        sales=sales,
        total_revenue=total_revenue,
        today_revenue=today_revenue
    )

if __name__ == "__main__":
    app.run(debug=True)

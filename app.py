from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def db():
    conn = sqlite3.connect('bulk.db')
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        quantity INTEGER
    )
    """)
    conn.commit()
    conn.close()

db()

@app.route("/")
def home():
    conn = sqlite3.connect("bulk.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template("index.html", products=products)

@app.route("/submit", methods=["POST"])
def submit():
    product = request.form.get("name")
    quantity = request.form.get("quantity")

    conn = sqlite3.connect("bulk.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, quantity) VALUES (?, ?)",
        (product, quantity)
    )
    conn.commit()
    conn.close()

    return "Product saved successfully! <br><a href='/'>Go Back</a>"

if __name__ == "__main__":
    app.run(debug=True)
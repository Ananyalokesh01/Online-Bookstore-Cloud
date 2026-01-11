from flask import Flask, render_template, request, redirect, url_for, flash
from db_connection import create_tables
from models import (
    add_book, get_books_in_stock, update_book, delete_book,
    add_customer, get_customers, update_customer, delete_customer,
    get_orders, place_order, delete_order, search_books, get_book_details
)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flashing messages

# ---------- ROUTES ---------- #

# Home Page
@app.route('/')
def index():
    books = get_books_in_stock()
    return render_template('index.html', books=books)

# ---------- BOOK ROUTES ---------- #

@app.route('/add_book', methods=['GET', 'POST'])
def add_book_view():
    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        price = request.form['price']
        stock = request.form['stock']
        
        if not title or not price or not stock:
            flash("All fields are required!", "danger")
        else:
            try:
                add_book(title, author_id, float(price), int(stock))
                flash("Book added successfully!", "success")
                return redirect(url_for('index'))
            except Exception as e:
                flash(f"Error: {str(e)}", "danger")
    
    return render_template('add_book.html')

@app.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book_view(book_id):
    book_details = get_book_details(book_id)
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        stock = request.form['stock']
        
        if not title or not price or not stock:
            flash("All fields are required!", "danger")
        else:
            try:
                update_book(book_id, title, float(price), int(stock))
                flash("Book updated successfully!", "success")
                return redirect(url_for('index'))
            except Exception as e:
                flash(f"Error: {str(e)}", "danger")
    
    return render_template('update_book.html', book=book_details)

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book_view(book_id):
    try:
        delete_book(book_id)
        flash("Book deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('index'))

@app.route('/search_books', methods=['GET', 'POST'])
def search_books_view():
    if request.method == 'POST':
        query = request.form['query']
        books = search_books(query)
        return render_template('search_results.html', books=books, query=query)
    
    return render_template('search_books.html')

# ---------- CUSTOMER ROUTES ---------- #

@app.route('/customers')
def customers():
    customers = get_customers()
    return render_template('customers.html', customers=customers)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer_view():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        
        if not first_name or not email:
            flash("First name and email are required!", "danger")
        else:
            try:
                add_customer(first_name, last_name, email, phone)
                flash("Customer added successfully!", "success")
                return redirect(url_for('customers'))
            except Exception as e:
                flash(f"Error: {str(e)}", "danger")
    
    return render_template('add_customers.html')

@app.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
def update_customer_view(customer_id):
    customer = next((c for c in get_customers() if c['customer_id'] == customer_id), None)
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        
        try:
            update_customer(customer_id, first_name, last_name, email, phone)
            flash("Customer updated successfully!", "success")
            return redirect(url_for('customers'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
    
    return render_template('update_customer.html', customer=customer)

@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer_view(customer_id):
    try:
        delete_customer(customer_id)
        flash("Customer deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('customers'))

# ---------- ORDER ROUTES ---------- #

@app.route('/orders')
def orders():
    orders = get_orders()
    return render_template('orders.html', orders=orders)

@app.route('/place_order', methods=['GET', 'POST'])
def place_order_view():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        selected_books = request.form.getlist('books')  # Fetch selected books

        if not customer_id or not selected_books:
            flash("Please select a customer and at least one book!", "danger")
            return redirect(url_for('place_order_view'))

        try:
            # Calculate total price
            books = [get_book_details(int(book_id)) for book_id in selected_books]
            total_price = sum(book['price'] for book in books)

            # Place the order
            order_id = place_order(int(customer_id), total_price)

            # Add order details and update stock
            for book_id in selected_books:
                book = get_book_details(int(book_id))
                if book['stock'] < 1:
                    flash(f"Book '{book['title']}' is out of stock!", "danger")
                    continue
                update_book(int(book_id), book['title'], book['price'], book['stock'] - 1)

            flash(f"Order #{order_id} placed successfully!", "success")
            return redirect(url_for('orders'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('place_order_view'))
            

    # Fetch customers and books to populate the form
    customers = get_customers()
    books = get_books_in_stock()  # Fetch books with stock > 0
    return render_template('place_order.html', customers=customers, books=books)




@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order_view(order_id):
    try:
        delete_order(order_id)
        flash("Order deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('orders'))

# ---------- APP START ---------- #

if __name__ == "__main__":
    create_tables()  # Ensure tables are created on startup
    app.run(host="0.0.0.0", port=5000)


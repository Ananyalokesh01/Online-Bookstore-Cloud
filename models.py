from db_connection import connect_to_database

# Helper function for executing queries
def execute_query(query, params=None, fetchone=False, fetchall=False):
    connection = connect_to_database()
    if not connection:
        raise Exception("Failed to connect to the database.")

    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if fetchone:
            result = cursor.fetchone()
            return dict(result) if result else None

        if fetchall:
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        connection.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close()
        connection.close()


# CRUD for Books
def add_book(title, author_id, price, stock):
    execute_query(
        "INSERT INTO books (title, author_id, price, stock) VALUES (?, ?, ?, ?)",
        (title, author_id, price, stock)
    )

def get_books_in_stock():
    return execute_query(
        "SELECT book_id, title, price, stock FROM books WHERE stock > 0",
        fetchall=True
    )

def update_book(book_id, title, price, stock):
    execute_query(
        "UPDATE books SET title = ?, price = ?, stock = ? WHERE book_id = ?",
        (title, price, stock, book_id)
    )

def delete_book(book_id):
    execute_query("DELETE FROM books WHERE book_id = ?", (book_id,))


# CRUD for Customers
def add_customer(first_name, last_name, email, phone):
    execute_query(
        "INSERT INTO customers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
        (first_name, last_name, email, phone)
    )

def get_customers():
    return execute_query(
        "SELECT customer_id, first_name, last_name, email, phone FROM customers",
        fetchall=True
    )

def update_customer(customer_id, first_name, last_name, email, phone):
    execute_query(
        "UPDATE customers SET first_name = ?, last_name = ?, email = ?, phone = ? WHERE customer_id = ?",
        (first_name, last_name, email, phone, customer_id)
    )

def delete_customer(customer_id):
    execute_query("DELETE FROM customers WHERE customer_id = ?", (customer_id,))


# CRUD for Orders
def get_orders():
    return execute_query(
        """
        SELECT o.order_id, o.customer_id, o.order_date, o.total_price
        FROM orders o
        """,
        fetchall=True
    )

def place_order(customer_id, total_price):
    execute_query(
        "INSERT INTO orders (customer_id, total_price) VALUES (?, ?)",
        (customer_id, total_price)
    )

def delete_order(order_id):
    execute_query("DELETE FROM orders WHERE order_id = ?", (order_id,))


# Search Books
def search_books(query):
    return execute_query(
        "SELECT book_id, title, price, stock FROM books WHERE title LIKE ?",
        ('%' + query + '%',),
        fetchall=True
    )

def get_book_details(book_id):
    return execute_query(
        "SELECT book_id, title, price, stock FROM books WHERE book_id = ?",
        (book_id,),
        fetchone=True
    )

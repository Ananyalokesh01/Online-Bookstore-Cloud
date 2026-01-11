import sqlite3

DB_NAME = "bookstore.db"

def connect_to_database():
    try:
        connection = sqlite3.connect(DB_NAME, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        print("Connected to SQLite database!")
        return connection
    except Exception as err:
        print(f"Error: {err}")
        return None


def create_tables():
    connection = connect_to_database()
    if not connection:
        print("Failed to connect to database")
        return

    cursor = connection.cursor()

    try:
        # Create authors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL
            )
        """)

        # Create books table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES authors(author_id)
            )
        """)

        # Create customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT
            )
        """)

        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                order_date TEXT DEFAULT CURRENT_TIMESTAMP,
                total_price REAL NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        """)

        # Create order_details table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_details (
                order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                book_id INTEGER,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        """)

        connection.commit()
        print("SQLite tables created successfully!")

    except Exception as err:
        print(f"Error while creating tables: {err}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    create_tables()

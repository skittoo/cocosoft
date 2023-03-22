import psycopg2

class CarHiringSystemDatabase:
    def __init__(self, host, user, password, db, port):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port

    def create_vehicle_table(self):
        conn = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db, port=self.port)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle (
                vehicle_id SERIAL PRIMARY KEY,
                category_id INT NOT NULL REFERENCES vehicle_category(category_id),
                availability VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def create_vehicle_category_table(self):
        conn = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db, port=self.port)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_category (
                category_id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def create_customer_table(self):
        conn = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db, port=self.port)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                customer_id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                phone_number VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def create_booking_table(self):
        conn = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db, port=self.port)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS booking (
                booking_id SERIAL PRIMARY KEY,
                customer_id INT NOT NULL REFERENCES customer(customer_id),
                vehicle_id INT NOT NULL REFERENCES vehicle(vehicle_id),
                start_date DATE NOT NULL,
                end_date DATE NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def create_invoice_table(self):
        conn = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db, port=self.port)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoice (
                invoice_id SERIAL PRIMARY KEY,
                booking_id INT NOT NULL REFERENCES booking(booking_id),
                amount DECIMAL(10,2) NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def add_customer(self, name, phone_number, email):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db
            )
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO customer (name, phone_number, email)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (name, phone_number, email))
            conn.commit()
            print(f"[INFO] Customer {name} added successfully")
            conn.close()
        except psycopg2.Error as e:
            print("Error adding customer:", e)

    def update_customer(self, customer_id, name=None, phone_number=None, email=None):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db
            )
            cursor = conn.cursor()
            update_query = "UPDATE customer SET "
            update_params = []
            if name:
                update_query += "name = %s, "
                update_params.append(name)
            if phone_number:
                update_query += "phone_number = %s, "
                update_params.append(phone_number)
            if email:
                update_query += "email = %s, "
                update_params.append(email)
            # remove trailing comma and space
            update_query = update_query[:-2]
            update_query += " WHERE customer_id = %s"
            update_params.append(customer_id)
            cursor.execute(update_query, tuple(update_params))
            conn.commit()
            print(f"[INFO] Customer {customer_id} updated successfully")
            conn.close()
        except psycopg2.Error as e:
            print("Error updating customer:", e)

    def get_customer(self, customer_id):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, phone_number, email FROM customer WHERE customer_id = %s
            """, (customer_id,))
            customer = cursor.fetchone()
            conn.close()
            if customer:
                return customer
            else:
                return None
        except psycopg2.Error as e:
            print("Error getting customer:", e)


    def delete_customer(self, customer_id):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customer WHERE customer_id = %s", (customer_id,))
            conn.commit()
            conn.close()
        except psycopg2.Error as e:
            print("Error deleting customer:", e)


    def print_all_tables(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db
            )
            cursor = conn.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            for table in tables:
                print(f"[INFO] EXISTS {table[0]}")
            conn.close()
        except psycopg2.Error as e:
            print("Error accessing the database:", e)

    def check_connection(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db
            )
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("Connection successful")
                conn.close()
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)


    def create_all_tables(self):
        self.create_vehicle_category_table()
        self.create_vehicle_table()
        self.create_customer_table()
        self.create_booking_table()
        self.create_invoice_table()
    

    def get_latest_customer_id(self):
        conn = psycopg2.connect(
            host=self.host,
            database=self.db,
            user=self.user,
            password=self.password
        )
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id FROM customer ORDER BY customer_id DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            latest_customer_id = result[0]
        else:
            latest_customer_id = None
        conn.close()
        return latest_customer_id

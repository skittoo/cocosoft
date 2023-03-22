from system_db import CarHiringSystemDatabase

def main():
    db_client = CarHiringSystemDatabase(
        db="car-hire",
        host="127.0.0.1",
        port= 5432, 
        user="postgres",
        password="root"
    )
    db_client.check_connection()
    db_client.create_all_tables()
    db_client.print_all_tables()
    
if __name__ == '__main__':
    main()

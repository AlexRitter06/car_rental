

import sqlite3

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Car:
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    registration_number: Optional[str] = None
    current_mileage: Optional[int] = None
    status: Optional[str] = None
    car_type: str = "regular_car"
    car_id: Optional[int] = None

@dataclass
class Customer:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    driver_license_number: Optional[str] = None
    address: Optional[str] = None
    customer_id: Optional[int] = None


class CarRentalDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()

    # =================================================================
    #      CAR
    # =================================================================
    def create_car(self, car: Car):
        sql = '''INSERT INTO cars (make, model, year, registration_number, current_mileage, status, car_type)
                 VALUES (?, ?, ?, ?, ?, ?, ?)'''
        self.cur.execute(sql, (car.make, car.model, car.year, car.registration_number, car.current_mileage, car.status, car.car_type))
        self.conn.commit()
        return self.cur.lastrowid

    def read_car(self, car_id):
        sql = 'SELECT * FROM cars WHERE car_id = ?'
        self.cur.execute(sql, (car_id,))
        result = self.cur.fetchone()
        if result:
            return Car(*result[1:], car_id=result[0])  # Skipping car_id in constructor and setting it manually
        return None

    def update_car(self, car: Car):
        sql = '''UPDATE cars
                 SET make = ?, model = ?, year = ?, registration_number = ?, current_mileage = ?, status = ?, car_type = ?
                 WHERE car_id = ?'''
        self.cur.execute(sql, (car.make, car.model, car.year, car.registration_number, car.current_mileage, car.status, car.car_type, car.car_id))
        self.conn.commit()

    def delete_car(self, car_id):
        sql = 'DELETE FROM cars WHERE car_id = ?'
        self.cur.execute(sql, (car_id,))
        self.conn.commit()


    def car_exists(self, car_id: int) -> bool:
        sql = 'SELECT 1 FROM cars WHERE car_id = ?'
        self.cur.execute(sql, (car_id,))
        return self.cur.fetchone() is not None


    # =================================================================
    #      Customers
    # =================================================================


    def create_customer(self, customer: Customer):
        sql = '''INSERT INTO customers (first_name, last_name, email, phone_number, driver_license_number, address)
                 VALUES (?, ?, ?, ?, ?, ?)'''
        self.cur.execute(sql, (customer.first_name, customer.last_name, customer.email, customer.phone_number, customer.driver_license_number, customer.address))
        self.conn.commit()
        return self.cur.lastrowid

    def read_customer(self, customer_id):
        sql = 'SELECT * FROM customers WHERE customer_id = ?'
        self.cur.execute(sql, (customer_id,))
        result = self.cur.fetchone()
        if result:
            return Customer(*result[1:], customer_id=result[0])  # Assign customer_id after unpacking
        return None

    def update_customer(self, customer: Customer):
        sql = '''UPDATE customers
                 SET first_name = ?, last_name = ?, email = ?, phone_number = ?, driver_license_number = ?, address = ?
                 WHERE customer_id = ?'''
        self.cur.execute(sql, (customer.first_name, customer.last_name, customer.email, customer.phone_number, customer.driver_license_number, customer.address, customer.customer_id))
        self.conn.commit()

    def delete_customer(self, customer_id):
        sql = 'DELETE FROM customers WHERE customer_id = ?'
        self.cur.execute(sql, (customer_id,))
        self.conn.commit()

    def customer_exists(self, customer_id: int) -> bool:
        sql = 'SELECT 1 FROM customers WHERE customer_id = ?'
        self.cur.execute(sql, (customer_id,))
        return self.cur.fetchone() is not None


# =================================================================
#
# =================================================================




def run_car_test():
    # Initialize the database handler

    db_path = "C:/Users/ritte/_PR_DEV_/DEV_PROJECTS_GIT/car_rental/sqlite_db/car_rental_db"
    db = CarRentalDatabase(db_path)

    # Create a new car
    new_car = Car(make="Honda", model="Civic", year=2020, registration_number="ABC123", current_mileage=10000,
                  status="available")
    car_id = db.create_car(new_car)
    new_car.car_id = car_id  # Update the car_id in the Car instance

    assert(db.car_exists(car_id))

    # Read a car's details
    car = db.read_car(car_id)
    print(car)

    # Update a car's details
    car.current_mileage = 12000
    db.update_car(car)

    # Delete a car
    db.delete_car(car_id)

    # Close the database connection
    db.close()


def run_customer_test():
    db_path = "C:/Users/ritte/_PR_DEV_/DEV_PROJECTS_GIT/car_rental/sqlite_db/car_rental_db"
    db = CarRentalDatabase(db_path)

    # Create a new customer without using the constructor for initial values
    new_customer = Customer()
    new_customer.first_name = "John"
    new_customer.last_name = "Doe"
    new_customer.email = "john.doe@example.com"
    new_customer.phone_number = "+123456789"
    new_customer.driver_license_number = "D12345678"
    new_customer.address = "123 Main St"

    # Create the new customer in the database
    customer_id = db.create_customer(new_customer)

    assert (db.customer_exists(customer_id))
    # Update the customer_id in the Customer instance
    new_customer.customer_id = customer_id

    # Read a customer's details
    customer = db.read_customer(customer_id)
    print(customer)

    # Update a customer's details
    customer.phone_number = "+987654321"
    db.update_customer(customer)

    # Delete a customer
    db.delete_customer(customer_id)

    # Close the database connection when done
    db.close()
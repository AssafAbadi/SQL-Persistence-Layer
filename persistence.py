import sqlite3
import atexit
from dbtools import Dao

 
# Data Transfer Objects:
class Employee(object):
     def __init__(self, id, name, salary,branche):
        self.id = id
        self.name = name
        self.salary = salary
        self.branche = branche


 
class Supplier(object):
        def __init__(self, id, name, contact_information):
            self.id = id
            self.name = name
            self.contact_information = contact_information



class Product(object):
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity
        



class Branche(object):
    def __init__(self, id, location,number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees
       

class Activitie(object):
    def __init__(self,product_id, quantity,activator_id,date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date

class Employee_Report:
    def __init__(self, name, salary, location, income):
        self.name = name
        self.salary = salary
        self.location = location
        self.total = income


 
#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        self.activities = Dao(type(Activitie),self._conn,"activitie")
        self.employees = Dao(type(Employee),self._conn,"employee")
        self.suppliers = Dao(type(Supplier),self._conn,"supplier")
        self.products = Dao(type(Product),self._conn,"product") 
        self.branches = Dao(type(Branche),self._conn,"branche")
        

    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branche    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()
 
    def emprep(self,conn):           
        print("Employees report")
        cursor =conn.cursor()
        all = cursor.execute("""SELECT employees.name, employees.salary, branches.location,
                             COALESCE(SUM((activities.quantity * products.price*(-1))),0) as income
                            FROM employees
                            LEFT JOIN branches ON employees.branche=branches.id
                            LEFT JOIN activities ON employees.id=activities.activator_id
                            LEFT JOIN products ON activities.product_id=products.id
                            GROUP BY employees.id
                            ORDER BY employees.name ASC;
                              """).fetchall()
        for row in all:
                print(*row,flush=True)
        cursor.close()
        
    def actrep(self,conn):
            print("Activities report")
            cursor = conn.cursor()
            all=cursor.execute("""SELECT a.date, p.description, a.quantity, ifnull(e.name,"None"),ifnull(s.name,"None")
            FROM activities a
            JOIN products p on p.id=a.product_id
            LEFT JOIN employees e on e.id=a.activator_id
            LEFT JOIN suppliers s on s.id=a.activator_id
            ORDER BY date ASC""").fetchall()
            for row in all:
                new_row = [f"'{val}'" if isinstance(val, str) and val != 'None' else val for val in row]
                print(f"({', '.join(map(str,new_row))})",flush=True)
            cursor.close()

# singleton
repo = Repository()
atexit.register(repo._close)
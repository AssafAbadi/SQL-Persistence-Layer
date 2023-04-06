from persistence import *
import sys
import os

def add_branche(splittedline : list[str]):
    branche=Branche(splittedline[0],splittedline[1],splittedline[2])
    temp=Dao(branche,repo._conn,"branche")
    temp.insert(temp._dto_type)       

def add_supplier(splittedline : list[str]):
    supplier=Supplier(splittedline[0],splittedline[1],splittedline[2])
    temp=Dao(supplier,repo._conn,"supplier")
    temp.insert(temp._dto_type)       

def add_product(splittedline : list[str]):
    product=Product(splittedline[0],splittedline[1],splittedline[2],splittedline[3])
    temp=Dao(product,repo._conn,"product")
    temp.insert(temp._dto_type)    

def add_employee(splittedline : list[str]):
    employee=Employee(splittedline[0],splittedline[1],splittedline[2],splittedline[3])
    temp=Dao(employee,repo._conn,"employee")
    temp.insert(temp._dto_type)
    

adders = {  "B": add_branche,
            "S": add_supplier,
            "P": add_product,
            "E": add_employee}

def main(args : list[str]):
    inputfilename = args[1]
    # delete the database file if it exists
    repo._close()
    # uncomment if needed
    if os.path.isfile("bgumart.db"):
        os.remove("bgumart.db")
    repo.__init__()
    repo.create_tables()
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(",")
            func = adders.get(splittedline[0])
            if func is not None:
                func(splittedline[1:])
        repo._conn.commit()
                
if __name__ == '__main__':
    main(sys.argv)
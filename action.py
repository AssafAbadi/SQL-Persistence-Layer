from persistence import *

import sys

def main(args : list[str]):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            product_id = splittedline[0]
            new_quantity = int(splittedline[1])
            activator_id = splittedline[2]
            date= splittedline[3]
            product=Dao(Product(product_id,"null",0,0),repo._conn,"product")
            temp=Dao.check_quantity(product)
            if(temp is not None):
                oldquan=temp[0]
                updatequan=oldquan+new_quantity
                if(updatequan>=0):
                    product.update_quantity(updatequan)
                    repo._conn.commit()
                    activitie=Activitie(product_id,new_quantity,activator_id,date)
                    act=Dao(activitie,repo._conn,"activitie")
                    act.insert(activitie)
                    repo._conn.commit()

             


if __name__ == '__main__':
    main(sys.argv)
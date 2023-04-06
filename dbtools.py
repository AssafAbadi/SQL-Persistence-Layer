import inspect

def orm(cursor, dto_type):
    # the following line retrieve the argument names of the constructor
    args = inspect.getargspec(dto_type.__init__).args

    # the first argument of the constructor will be 'self', it does not correspond
    # to any database field, so we can ignore it.
    args = args[1:]

    # gets the names of the columns returned in the cursor
    col_names = [column[0] for column in cursor.description]

    # map them into the position of the corresponding constructor argument
    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]


def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)


class Dao(object):
    def __init__(self, dto_type, conn,name):
        self._conn = conn
        self._dto_type = dto_type
        self.name=name.lower()+'s'
        
       


    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)

        column_names = ','.join(ins_dict.keys())
        params = list(ins_dict.values())
        qmarks = ','.join(['?'] * len(ins_dict))

        stmt = 'INSERT INTO {} ({}) VALUES ({})' \
            .format(self.name, column_names, qmarks)

        self._conn.execute(stmt, params)

    def find_all(self):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {}'.format(self.name))
        return orm(c, self._dto_type)
    
    def find(self, **keyvals):
        column_names = keyvals.keys()
        params = list(keyvals.values())
 
        stmt = 'SELECT * FROM {} WHERE {}' \
               .format(self.name, ' AND '.join([col + '=?' for col in column_names]))
 
        c = self._conn.cursor()
        c.execute(stmt, params)
        return orm(c, self._dto_type)

    def delete(self, **keyvals):
        column_names = keyvals.keys()
        params = list(keyvals.values())
 
        stmt = 'DELETE FROM {} WHERE {}' \
               .format(self.name,' AND '.join([col + '=?' for col in column_names]))
 
        self._conn.cursor().execute(stmt, params)

    def check_quantity(self):
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT quantity FROM products WHERE id = ?
                """, [self._dto_type.id])
            data = cursor.fetchone()
            cursor.close()
            return data
                        


    def update_quantity(self, new_quantity):
            cursor = self._conn.cursor()
            cursor.execute("""
                UPDATE products SET quantity = ? WHERE id = ?
                """, [new_quantity, self._dto_type.id])
            self._conn.commit()    
            cursor.close()

    def prints(self,conn):
        cursor = conn.cursor()
        table_name = self.name.capitalize()
        print(table_name,flush=True)
        if table_name == 'Activities':
             cursor.execute("SELECT * FROM {} ORDER BY date ASC".format(self.name))
        else:
             cursor.execute("SELECT * FROM {} ORDER BY id ASC".format(self.name))
        data = cursor.fetchall()
        for record in data:
            if (table_name == 'Activities'):
              print("(%d, %d, %d, '%s')" % (record[0], record[1], record[2],record[3]),flush=True)
            elif table_name == 'Branches':
               print("(%d, '%s',  %d)" % (record[0], record[1], record[2]),flush=True)
            elif table_name == 'Employees':
                print("(%d, '%s',  %.1f, %d)" % (record[0], record[1], record[2],record[3]),flush=True)
            elif table_name == 'Products':
                print("(%d, '%s',  %.1f, %d)" % (record[0], record[1], record[2],record[3]),flush=True)
            elif table_name == 'Suppliers':
                print("(%d, '%s', '%s')" % (record[0], record[1], record[2]),flush=True)
        cursor.close()


    
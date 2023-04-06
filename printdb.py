from persistence import *


def main():
    with sqlite3.connect('bgumart.db') as conn:
        repo.activities.prints(conn)
        conn.commit()
        repo.branches.prints(conn)
        conn.commit()
        repo.employees.prints(conn)
        conn.commit()
        repo.products.prints(conn)
        conn.commit()
        repo.suppliers.prints(conn)
        conn.commit()
        print("",flush=True)
        repo.emprep(conn)
        conn.commit()
        print("",flush=True)
        repo.actrep(conn)
        conn.commit()


if __name__ == '__main__':
    main()
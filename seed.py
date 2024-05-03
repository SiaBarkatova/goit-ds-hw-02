from sqlite3 import Error
from connect import create_connection, database
from faker import Faker




#def create_task(conn, task):

def create_user(conn, user):
    sql = '''
    INSERT INTO users(fullname, email) VALUES(?,?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, user)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid

def create_status(conn, status):
    sql = '''
    INSERT INTO status(name) VALUES(?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, status)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid


with create_connection(database) as conn:

    #add static stasuses
    statuses = [('new',), ('in progress',), ('completed',)]
    for status in statuses:  
        pass   
    #   create_status(conn, status)

    #add random users
    fake = Faker("uk-UA")
    for _ in range(20):
        create_user(conn, (fake.name(), fake.email()))

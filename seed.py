from sqlite3 import Error

from connect import create_connection, database

import random

from faker import Faker


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

def create_task(conn, task):
    sql = '''
    INSERT INTO tasks(title, description, status_id, user_id) VALUES(?,?,?,?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, task)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid


if __name__ == '__main__':
    with create_connection(database) as conn:

        #add static stasuses
        statuses = [('new',), ('in progress',), ('completed',)]
        
        #gather ids for following seeding of taks
        status_ids = []
        for status in statuses:  
            status_ids.append(create_status(conn, status))

        print("3 statuses added successfully.")

        #add 20 random users using faker
        fake = Faker("uk-UA")
        num_users = 0
        num_tasks = 0
        for _ in range(20):
            user_id = create_user(conn, (fake.name(), fake.email()))
            num_users += 1

            # for each user and for each status we create task (3 tasks per user)
            for status_id in status_ids:
                if random.randint(0,2) > 0: # skip 2/3 of potential created tasks
                    continue

                task = (fake.sentence(nb_words=4), fake.paragraph(nb_sentences=3), status_id, user_id)
                create_task(conn, task)
                num_tasks += 1

        print(f"{num_users} users and {num_tasks} taks added successfully.")

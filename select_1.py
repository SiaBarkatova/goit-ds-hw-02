from sqlite3 import Error

from connect import create_connection, database
from faker import Faker

def select_tasks_by_user_id(conn, user_id):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_users_by_mail_service(conn, mail_service):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email LIKE ?", ('%' + mail_service,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_tasks_by_status(conn, status):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name=?);", (status,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_users_without_tasks(conn):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def update_task_status(conn, task_id, status):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE tasks SET status_id=(SELECT id FROM status WHERE name=?) WHERE id = ?;", (status, task_id))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

def add_task_for_user(conn, title, task, user_id, status):

    cur = conn.cursor()
    try:
        
        cur.execute("SELECT id FROM status WHERE name=?", (status,))
        status_id = cur.fetchone()

        sql = '''
        INSERT INTO tasks(title, description, status_id, user_id) VALUES(?,?,?,?);
        '''
        cur.execute(sql, (title, task, status_id[0], user_id))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

def delete_task_by_id(conn, task_id):

    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
        conn.commit()
        print(f"Deleted {cur.rowcount} tasks.")  
    except Error as e:
        print(e)
    finally:
        cur.close()


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return: rows tasks
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_all_not_completed_tasks(conn):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM tasks WHERE status_id <> (SELECT id FROM status WHERE name=?);",("completed",))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_task_by_status(conn, status):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param status:
    :return: rows tasks
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE status=?", (status,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

if __name__ == '__main__':
    with create_connection(database) as conn:
        # print("Users:")
        # users = select_users(conn)
        # print(users)
        # print("\\nQuery all tasks")
        # tasks = select_all_tasks(conn)
        # print(tasks)
        # print("\\nQuery task by status:")
        # task_by_priority = select_task_by_status(conn, True)
        # print(task_by_priority)
        # print(select_tasks_by_user_id(conn, 7))
        # print(select_tasks_by_status(conn, 'new'))
        # update_task_status(conn, 16, "completed")
        # print(select_users_without_tasks(conn))

        # fake = Faker("uk-UA")
        # user_id = 8
        # task = fake.paragraph(nb_sentences=3)
        # title = "Виконати задачу швидко"
        # add_task_for_user(conn, title, task, user_id, "new")
        # print(select_all_not_completed_tasks(conn))
        # delete_task_by_id(conn, 11)
        print(select_users_by_mail_service(conn, "example.com"))

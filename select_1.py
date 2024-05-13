from sqlite3 import Error

from connect import create_connection, database
from faker import Faker

def select_tasks_by_user_id(conn, user_id): # 1 Отримати всі завдання певного користувача
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

def select_tasks_by_status(conn, status): # 2 Вибрати завдання за певним статусом
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

def update_task_status(conn, task_id, status): # 3 Оновити статус конкретного завдання
    cur = conn.cursor()
    try:
        cur.execute("UPDATE tasks SET status_id=(SELECT id FROM status WHERE name=?) WHERE id = ?;", (status, task_id))
        conn.commit()
        print("Task successfully updated, new status is: " + status)

    except Error as e:
        print(e)
    finally:
        cur.close()

def select_users_without_tasks(conn): # 4 Отримати список користувачів, які не мають жодного завдання
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

def add_task_for_user(conn, title, task, user_id, status): # 5 Додати нове завдання для конкретного користувача
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM status WHERE name=?", (status,))
        status_id = cur.fetchone()

        sql = '''
        INSERT INTO tasks(title, description, status_id, user_id) VALUES(?,?,?,?);
        '''
        cur.execute(sql, (title, task, status_id[0], user_id))
        conn.commit()
        print("New task succesfully added for user: " + str(user_id))

    except Error as e:
        print(e)
    finally:
        cur.close()

def select_all_not_completed_tasks(conn): # 6 Отримати всі завдання, які ще не завершено
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

def delete_task_by_id(conn, task_id): # 7 Видалити конкретне завдання
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
        conn.commit()
        print(f"Deleted {cur.rowcount} tasks.")  
    except Error as e:
        print(e)
    finally:
        cur.close()

def select_users_by_mail_service(conn, mail_service): # 8 Знайти користувачів з певною електронною поштою
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

def update_user_name(conn, fullname, user_id): # 9 Оновити ім'я користувача

    sql = '''
    UPDATE users 
    SET fullname=?
    WHERE id = ?;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, (fullname, user_id))
        conn.commit()
        print("User name updated. New name: " + fullname)

    except Error as e:
        print(e)
    finally:
        cur.close()

def select_task_quantity_by_status(conn): # 10 Отримати кількість завдань для кожного статусу

    sql = """
    SELECT s.name, COUNT(*)    
    FROM tasks t
    LEFT JOIN status s ON t.status_id = s.id
    GROUP BY t.status_id;
    """

    rows = None
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_tasks_by_user_mail_service(conn, mail_service): # 11 Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
    rows = None
    cur = conn.cursor()

    sql = """
    SELECT t.id, t.title, u.email 
    FROM tasks t
    LEFT JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE ?
    """
    try:
        cur.execute(sql, ('%' + mail_service,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_tasks_whithout_description(conn): # 12 Отримати список завдань, що не мають опису

    rows = None
    cur = conn.cursor()
    
    sql = """SELECT t.id, t.title, t.description 
    FROM tasks t
    WHERE t.description is null or t.description = ''
    """
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_users_and_tasks_by_status(conn, status): # 13 Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
    rows = None
    cur = conn.cursor()

    sql = """
    SELECT t.id,  u.fullname, t.title, s.name 
    FROM tasks t
    INNER JOIN users u ON t.user_id = u.id
    LEFT JOIN status s ON t.status_id = s.id
    WHERE s.name = ?
    """
    try:
        cur.execute(sql, (status,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_task_quantity_by_user(conn): # 14 Отримати користувачів та кількість їхніх завдань

    sql = """
    SELECT u.fullname, COUNT(t.user_id)
    FROM users u
    LEFT JOIN tasks t ON t.user_id = u.id
    GROUP BY u.fullname;
    """

    rows = None
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


if __name__ == '__main__':
    with create_connection(database) as conn:
        
        print("Tasks selected by User ID:")
        print(select_tasks_by_user_id(conn, 7)) # 1
        print("")

        print("Tasks selected by Status:")
        print(select_tasks_by_status(conn, 'new')) # 2
        print("")

        update_task_status(conn, 16, "completed") # 3
        print("")

        print("Users without tasks:")
        print(select_users_without_tasks(conn)) # 4
        print("")

        fake = Faker("uk-UA") # 5
        user_id = 8 # 5
        task = fake.paragraph(nb_sentences=3) # 5
        title = "Виконати задачу швидко" # 5
        add_task_for_user(conn, title, task, user_id, "new") # 5
        print("")


        print("Not completed tasks:")
        print(select_all_not_completed_tasks(conn)) # 6
        print("")

        delete_task_by_id(conn, 11) # 7
        print("")

        print("Users with email example.com")
        print(select_users_by_mail_service(conn, "example.com")) # 8
        print("")

        update_user_name(conn, "Taras Shevchenko", 9) # 9
        print("")

        print("Count tasks by statuses:")
        print(select_task_quantity_by_status(conn)) # 10
        print("")

        print("Tasks by users email address: example.net")
        tasks = select_tasks_by_user_mail_service(conn, "example.net") # 11
        for task in tasks: # 11
           print(task) # 11
        print("")

        print("Tasks with empty description:")
        print(select_tasks_whithout_description(conn)) # 12
        print("")

        print("Users with tasks by status: in progress")
        tasks = select_users_and_tasks_by_status(conn, "in progress") # 13
        for task in tasks: # 13
            print(task) # 13
        print("")

        print("Nubmers of tasks by user:")
        print(select_task_quantity_by_user(conn)) # 14
        print("")

import calendar
import operator
from itertools import groupby
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="",
    password="",
    database="mydatabase"
)

mycursor = mydb.cursor()


def get_tasks_from_database():
    sql = "SELECT id, title, taskDate, task_status FROM tasks"
    mycursor.execute(sql)
    my_tasks = mycursor.fetchall()

    tasks = []

    for task_id, task_title, task_date, task_status in my_tasks:
        task = {"id": task_id, "title": task_title, "date": task_date, "status": task_status}
        tasks.append(task)

    return tasks


def display_tasks(tasks):
    # sort tasks by date
    tasks.sort(key=operator.itemgetter("date"))

    # display tasks grouped by date
    for key, value in groupby(tasks, key=operator.itemgetter("date")):
        # print the date the day of the week
        print(str(key) + " " + calendar.day_name[key.weekday()])

        # print title of the task
        completed_title = ""
        for i in value:
            # if status is 'Completed' print the crossed out title, else print normally
            if i['status'] == "Completed":
                for x in i['title']:
                    completed_title = completed_title + x + '\u0336'
                print(completed_title)
            else:
                print("\t" + i["title"])
        print(30 * "-")


def display_menu():
    current_tasks = get_tasks_from_database()
    display_tasks(current_tasks)

    print("1) Add new task")
    print("2) Delete task")
    print("3) Edit task")
    print("4) Mark as completed")

    choice = " "
    acceptable_range = range(0, 5)
    within_range = False

    # check if input is not empty, is numeric and is in range
    while not choice.isnumeric() or len(choice) == 0 or not within_range:

        # keep asking for choice until the conditions are met
        choice = input("Choose number:")

        # numeric check
        if not choice.isnumeric():
            print("Input is not a number or is empty")

        # range check
        if choice.isnumeric():
            if int(choice) in acceptable_range:
                within_range = True
            else:
                print("There is no such an item in menu")
                within_range = False

    choice = int(choice)
    if choice == 1:
        add_new_task()
    elif choice == 2:
        delete_task(current_tasks)
    elif choice == 3:
        edit_task()
    elif choice == 4:
        mark_as_completed(current_tasks)


def add_new_task():
    new_task_title = ""
    new_task_date = None

    # check if input is not empty
    while not (new_task_title and new_task_title.strip()):

        new_task_title = input("Task title:")
        if new_task_title and new_task_title.strip():

            new_task_date = input("Task date in format YYYY-MM-DD: ")

            sql = "INSERT INTO tasks (title, taskDate) VALUES (%s, %s)"
            val = [
                (new_task_title, new_task_date)
            ]

            mycursor.executemany(sql, val)

            mydb.commit()

        else:
            print("You didn't enter any task!")


def delete_task(tasks):
    task_id = " "
    acceptable_ids = []
    within_range = False

    # get IDs of tasks
    for obj in tasks:
        acceptable_ids.append(obj['id'])

    # check if input is not empty, is numeric and task with the ID exist
    while not task_id.isnumeric() or len(task_id) == 0 or not within_range:

        task_id = input("Enter ID of the task you want to delete:")

        # numeric check
        if not task_id.isnumeric():
            print("Input is not a number or is empty")

        # range check
        if task_id.isnumeric():
            if int(task_id) in acceptable_ids:
                within_range = True
            else:
                print("There is no task with this ID")
                within_range = False

    mycursor.execute(f"DELETE FROM tasks WHERE id = {task_id}")
    mydb.commit()
    print(f'record with ID {task_id} deleted')


def edit_task():
    pass


def mark_as_completed(tasks):
    task_id = " "
    acceptable_ids = []
    within_range = False

    # get IDs of tasks
    for obj in tasks:
        acceptable_ids.append(obj['id'])

    # check if input is not empty, is numeric and task with the ID exist
    while not task_id.isnumeric() or len(task_id) == 0 or not within_range:

        task_id = input("Enter ID of the task you want to mark as completed:")

        # numeric check
        if not task_id.isnumeric():
            print("Input is not a number or is empty")

        # range check
        if task_id.isnumeric():
            if int(task_id) in acceptable_ids:
                within_range = True
            else:
                print("There is no task with this ID")
                within_range = False

    mycursor.execute(f"UPDATE tasks SET task_status = 'Completed' WHERE id = {task_id}")
    mydb.commit()
    print(f'record with ID {task_id} marked as completed')


# display warning if it's 7 or less days to task date
def display_warning():
    pass


def check_weather():
    pass


def main():
    display_menu()
    main()


if __name__ == "__main__":
    main()

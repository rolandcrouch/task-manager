from task_manager_build import Task, TaskManager
from user_manager import User, UserManager
import datetime
import os
import json

# Ensure the current directory is set correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("config.json", "r") as f:
    config = json.load(f)


def register_new(user_manager):
    """
    Adds a new user if the username is unique and 
    password confirmation matches.
    """

    while True:
        # Prompt for a new username
        new_username = input('\nEnter a new username: ').strip()

        # Check if username already exists in user list
        if any(user.username == new_username 
                                for user in user_manager.users):
            print("That username already exists. "
                  "Please choose another.")
            continue

        # Prompt for password and confirmation
        new_password = input('Enter a new password: ').strip()
        repeat_password = input('Confirm your password: ').strip()

        # Check if passwords match
        if new_password != repeat_password:
            print("Passwords do not match. Please try again.")
        else:
            user = User(new_username, new_password)
            user_manager.add_user(user)
            user_manager.save_users()

            print("New user registered successfully!\n")
            break


def get_valid_task_number(selection, user_tasks):
    """
    Validates the task number entered by the user.
    Prompts again if the input is not valid.
    """

    # Check if user wants to exit or has entered a valid selection
    if selection == -1 or \
        (selection >= 1 and selection <= len(user_tasks)):
        return selection
    else:
        try:
            # Prompt for input again if selection is invalid
            selection = int(input("\nEnter task number to manage "
                                  "or -1 to return to menu: "))
        except ValueError:
            print("\nPlease enter a valid number.")

        # Recursively validate the new input
        return get_valid_task_number(selection, user_tasks)


def view_user_tasks_input(task_manager,username):
    """
    Displays tasks assigned to the current user and 
    allows editing or marking them as complete.
    """

    while True:
        # Display user's tasks
        task_manager.view_user_tasks(username)
        user_tasks = [task for task in task_manager.tasks if 
                      task.username == username]

        # Prompt for task selection
        try:
            selection = int(input("\nEnter task number to manage "
                                  "or -1 to return to menu: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if selection == -1:
            break

        # Validate selected task number
        if selection < 1 or selection > len(user_tasks):
            selection = get_valid_task_number(selection, user_tasks)
            if selection == -1:
                break

        selected_task = user_tasks[selection - 1]

        # Action menu
        print("\nWhat would you like to do?")
        print("1  - Mark task as complete")
        print("2  - Edit task")
        print("-1 - Return to task main menu")

        option = input("\nEnter choice: ").strip()

        if option == '1':
            # Mark the task as complete
            selected_task.completed = "Yes"
            print("Task marked as complete.")
        
        elif option == '2':
            # Prevent editing of completed tasks
            if selected_task.completed == "Yes":
                print("Task already completed. Cannot edit.")
            else:
                # Edit assigned user
                new_user = input("Enter new username "
                                 "(or press Enter to skip): ").strip()
                if new_user:
                    selected_task.username = new_user

                # Edit due date with validation
                while True:
                    new_due = input("Enter new due date (dd:mm:yyyy) "
                                "(or press Enter to skip): ").strip()
                    if new_due == "":
                        break
                    try:
                        due_date = \
                        datetime.datetime.strptime(new_due, 
                                        config["date_format_input"])

                        selected_task.date_due = \
                        due_date.strftime(
                                    config["date_format_display"])

                        break
                    except ValueError:
                        print("❌ Invalid date format. " 
                        "Please use dd:mm:yyyy.")
        
        elif option == '-1':
            break
        else:
            print("Invalid selection.")

        print(f"\n[DEBUG] Total tasks in memory before saving: {len(task_manager.tasks)}")
        for t in task_manager.tasks:
            print(f" - {t.username} | {t.title} | {t.completed}")

        # Update tasks.txt with changes
        task_manager.save_tasks()


def add_task_input(task_manager, user_manager):
    """
    Assigns a new task to an existing user and writes it to file.
    """
    while True:
        # Ask for the username the task is being assigned to
        input_username = input('\nPlease enter the username for '
                               'which the task is being assigned: ')

        # Check if the username exists in the user list
        user_found = any(user.username == input_username 
                         for user in user_manager.users)

        if not user_found:
            print("\nUsername not found. Please try again.")
            continue  # Prompt again if username is invalid

        # Collect task title and description
        input_title = input("\nPlease enter the title of the task: ")
        input_description = \
            input("\nPlease enter the description of the task: ")

        # Get today's date for when the task is added
        input_add = datetime.date.today()
        formatted_add = input_add.strftime(
                        config["date_format_display"])

        # Prompt for and validate due date format
        while True:
            input_due_str = \
                input("Please enter the due date" \
                        " of the task (dd:mm:yyyy): ")
            try:
                input_due = datetime.datetime.  \
                        strptime(input_due_str, 
                                 config["date_format_input"])
                formatted_due = input_due.strftime(
                                config["date_format_display"])
                break
            except ValueError:
                print("Invalid date format. Please use dd:mm:yyyy.")

        # Create and add task
        task = Task(input_username, input_title, input_description,
                     formatted_add, formatted_due)
        task_manager.add_task(task)

        print("\nTask successfully assigned.")
        break


def delete_task_input(task_manager):
    """
    Allows admin to delete a selected task.
    Updates the tasks.txt file after deletion.
    """
    # Check if there are any tasks to delete
    if not task_manager.tasks:
        print("\nNo tasks available to delete.")
        return

    # Display task titles with assigned users
    print("\nAvailable Tasks:\n")
    for index, task in enumerate(task_manager.tasks, start=1):
        print(f"{index}. {task.title} (Assigned to: {task.username})")

    try:
        # Prompt for task number to delete
        choice =    \
            int(input("\nEnter the number of the task to delete: "))

        # Validate selection range and update
        if 1 <= choice <= len(task_manager.tasks):
            deleted_task = task_manager.tasks.pop(choice - 1)
            task_manager.save_tasks()
            print(f"\nTask '{deleted_task.title}' "
                  f"deleted successfully.")
        else:
            print("\nInvalid selection. No task deleted.")
    except ValueError:
        print("\nPlease enter a valid number.")
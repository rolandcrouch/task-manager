"""
task_manager.py

Defines Task and TaskManager classes.

Task: Represents individual tasks with relevant attributes and methods.
TaskManager: Manages reading, writing, 
and displaying tasks from tasks.txt.
"""

import os
import json

# Ensure the current directory is set correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("config.json", "r") as f:
    config = json.load(f)


class Task:

    def __init__(self, username, title, description, date_add, 
                 date_due, completed="No"):
        # Assign task details to object properties
        self.username = username
        self.title = title
        self.description = description
        self.date_add = date_add
        self.date_due = date_due
        self.completed = completed.capitalize()

    def mark_complete(self):
        """
        Marks this task as completed by setting completed to 'Yes'.
        """
        self.completed = "Yes"

    def to_file_string(self):
        """
        Returns a string representation of the task formatted 
        for file storage.
        """
        return f"{self.username}, {self.title}, {self.description}, " \
                f"{self.date_add}, {self.date_due}, {self.completed}"

    def __str__(self):
        """
        Returns a readable string representation of the task 
        for display.
        """
        return (f"User: {self.username}\nTitle: {self.title}"
                f"\nDescription: {self.description}\n"
                f"Added: {self.date_add}\nDue: {self.date_due}"
                f"\nCompleted: {self.completed}")


class TaskManager:

    def __init__(self, file_path=config["task_file"]):
        self.file_path = file_path
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """
        Reads tasks from 'tasks.txt' and loads them into self.tasks.
        Each line should contain: username, title, description, 
        date_add, date_due, completed
        """
        try:
            with open(self.file_path, "r") as f:
                for i, line in enumerate(f):
                    if i == 0 and "username" in line.lower():
                        continue  # skip header
                    fields = [field.strip() 
                          for field in line.strip().split(",")]
                    if len(fields) == 6:
                        self.tasks.append(Task(*fields))
        except FileNotFoundError:
            # Handle missing file gracefully
            print("tasks.txt not found")

    def save_tasks(self):
        """
        Saves all tasks to 'tasks.txt', overwriting the file.
        """
        with open(self.file_path, "w") as f:
            f.write("username, title, description, date_add, "
                    "date_due, Completed\n")
            for task in self.tasks:
                f.write(task.to_file_string() + "\n")

    def add_task(self, task):
        """
        Adds a new task to the list and saves it to the file.
        """
        self.tasks.append(task)
        with open(self.file_path, "a") as f:
            f.write(task.to_file_string() + "\n") 

    def delete_task(self, task):
        """
        Deletes a task at the given index from the task list 
        and updates the file.
        """
        self.tasks.pop(task)
        self.save_tasks()

    def display_task(self, task, index=None):
        """
        Prints task details in a formatted way, 
        including index if provided.
        """
        if index is not None:
            print(f"\nTask {index}")
        print(f"User        : {task.username}")
        print(f"Title       : {task.title}")
        print(f"Description : {task.description}")
        print(f"Date Added  : {task.date_add}")
        print(f"Due Date    : {task.date_due}")
        print(f"Completed   : {task.completed}")
        print("-" * 40)

    def view_all_tasks(self):
        """
        Displays all tasks in the system.
        """
        for index, task in enumerate(self.tasks, start=1):
            self.display_task(task, index)

    def view_user_tasks(self, username):
        """
        Displays all tasks assigned to a specific user.
        """
        user_tasks = [task for task in self.tasks 
                      if task.username == username]
        if not user_tasks:
            print(f"No tasks found for {username}")
        for index, task in enumerate(user_tasks, start=1):
            self.display_task(task, index)

    def view_completed_tasks(self):
        """
        Displays all tasks marked as completed.
        """
        completed_found = False  
        for index, task in enumerate(self.tasks, start=1):
            if str(task.completed).lower() in ['true', 'yes']:
                completed_found = True
                self.display_task(task, index)
        if not completed_found:
            print("No completed tasks found.")

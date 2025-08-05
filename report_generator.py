"""
report_generator.py

Defines the ReportGenerator class.

ReportGenerator: Generates task and user overview reports 
from task and user data,writes them to text files, 
and displays statistics summaries.
"""

import datetime
import os
from task_manager_build import Task, TaskManager
from user_manager import User, UserManager
import json

# Ensure the current directory is set correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("config.json", "r") as f:
    config = json.load(f)


class ReportGenerator:
    def __init__(self, task_manager, user_manager):
        self.tasks = task_manager.tasks
        self.users = user_manager.users

    def write_task_overview(self):
        """
        Creates task_overview.txt with statistics about tasks.
        """
        # Total number of tasks in the system
        total_tasks = len(self.tasks)

        # Count tasks that are marked as completed
        completed_tasks = sum(1 for task in self.tasks 
                          if task.completed.lower() == "yes")

        # Uncompleted tasks are the remaining tasks
        uncompleted_tasks = total_tasks - completed_tasks

        # Track overdue tasks (not completed and due before today)
        overdue_tasks = 0
        today = datetime.datetime.today()

        for task in self.tasks:
            try:
                # Parse the due date
                due_date = datetime.datetime.strptime(task.date_due, 
                                        config["date_format_display"])
                # Check if task is overdue and incomplete
                if task.completed.lower() == "no" and due_date < today:
                    overdue_tasks += 1
            except ValueError:
                # Skip tasks with invalid date format
                continue

        # Calculate percentages with protection against division by zero
        incomplete_percentage = (
            (uncompleted_tasks / total_tasks * 100) if total_tasks else 0
            )
        overdue_percentage = (
            (overdue_tasks / total_tasks * 100) if total_tasks else 0
            )

        # Write the statistics to task_overview.txt
        with open(config["task_overview_file"], "w") as f:
            f.write("=== Task Overview ===\n\n")
            f.write(f"Total number of tasks             : "
                f"{total_tasks}\n")
            f.write(f"Total number of completed tasks   : "
                f"{completed_tasks}\n")
            f.write(f"Total number of uncompleted tasks : "
                f"{uncompleted_tasks}\n")
            f.write(f"Total number of overdue tasks     : "
                f"{overdue_tasks}\n")
            f.write(f"Percentage of incomplete tasks    : "
                f"{incomplete_percentage:.2f}%\n")
            f.write(f"Percentage of overdue tasks       : "
                f"{overdue_percentage:.2f}%\n")
          

    def write_user_overview(self):
        """
        Writes user_overview.txt containing per-user task statistics.
        """
        total_users = len(self.users)
        total_tasks = len(self.tasks)

        # Create a dictionary to map each user to their tasks
        user_task_map = {user.username: [] for user in self.users}
        for task in self.tasks:
            if task.username in user_task_map:
                user_task_map[task.username].append(task)

        today = datetime.datetime.today()

        # Open the output file for writing user statistics
        with open(config["user_overview_file"], "w") as f:
            f.write("=== User Overview ===\n\n")
            f.write(f"Total number of users registered : "
                    f"{total_users}\n")
            f.write(f"Total number of tasks            : "
                    f"{total_tasks}\n\n")

            # Process stats for each user
            for user in self.users:
                username = user.username
                user_tasks = user_task_map.get(username, [])
                user_total = len(user_tasks)

                if user_total > 0:
                    # Calculate user-specific task stats
                    percent_assigned = (user_total / total_tasks) * 100
                    completed = sum(1 for t in user_tasks 
                                if t.completed.lower() == "yes")
                    incomplete = user_total - completed
                    overdue = 0

                    # Count overdue tasks
                    for task in user_tasks:
                        try:
                            due = datetime.datetime.    \
                                    strptime(task.date_due, 
                                        config["date_format_display"])  
                            if task.completed.lower() == "no" \
                                    and due < today:
                                overdue += 1
                        except ValueError:
                            continue  # Skip tasks with invalid dates

                    # Percentages of completed, incomplete, and overdue
                    percent_completed = (completed / user_total) * 100
                    percent_incomplete = (incomplete / user_total) * 100
                    percent_overdue = (overdue / user_total) * 100
                else:
                    # No tasks assigned to user
                    percent_assigned = percent_completed = \
                    percent_incomplete = percent_overdue = 0

                # Write user-specific stats to file
                f.write(f"User: {username}\n")
                f.write(f"  - Tasks assigned                 : "
                    f"{user_total}\n")
                f.write(f"  - % of total tasks assigned      : "
                    f"{percent_assigned:.2f}%\n")
                f.write(f"  - % completed                    : "
                    f"{percent_completed:.2f}%\n")
                f.write(f"  - % incomplete                   : "
                    f"{percent_incomplete:.2f}%\n")
                f.write(f"  - % overdue                      : "
                    f"{percent_overdue:.2f}%\n\n")
      

    def generate(self):
        self.write_task_overview()
        self.write_user_overview()
        # Notify user that reports were created successfully
        print("\nReports successfully generated: 'task_overview.txt'"
            " and 'user_overview.txt'")


    def display_statistics(self):
        """
        Displays task and user overview reports.
        If reports are missing, generates them first.
        """

        # Generate reports if they are not already present
        if not os.path.exists(config["task_overview_file"]) or not \
            os.path.exists(config["user_overview_file"]):
            print("\nReports not found. Generating reports first...")
            self.generate()

        # Display contents of task overview
        print("\nTASK OVERVIEW\n" + "═" * 40)
        try:
            with open(config["task_overview_file"], "r") as file:
                print(file.read())  # Print entire file content
        except FileNotFoundError:
            print("Could not find 'task_overview.txt'.")

        # Display contents of user overview
        print("\nUSER OVERVIEW\n" + "═" * 40)
        try:
            with open(config["user_overview_file"], "r") as file:
                print(file.read())  # Print entire file content
        except FileNotFoundError:
            print("Could not find 'user_overview.txt'.")
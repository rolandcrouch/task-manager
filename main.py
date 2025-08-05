from task_manager_build import Task, TaskManager
from user_manager import User, UserManager
from report_generator import ReportGenerator
from user_input import register_new, get_valid_task_number, \
                        view_user_tasks_input, add_task_input, \
                        delete_task_input
import os

# Ensure the current directory is set correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import json

with open("config.json", "r") as f:
        config = json.load(f)


def admin_menu(username, user_manager, task_manager, report_gen):
    """
    Displays the admin menu and handles admin-specific actions.
    Uses styled and aligned output for improved terminal appearance.
    """
    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RED = "\033[31m"

    while True:
        print(f"\n{BOLD}{CYAN}╔════════════════════════════════════"
              f"══╗{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}    {BOLD}{BLUE}ADMIN CONTROL MENU"
              f"{RESET}                {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}╠══════════════════════════════════════"
              f"╣{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}r.{RESET} "
              f"  Register a new user            {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}a.{RESET} "
              f"  Add a new task                 {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}va.{RESET}  "
              f"View all tasks                 {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}vm.{RESET}  "
              f"View user tasks                {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}vc.{RESET}  "
              f"View completed tasks           {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}del.{RESET} "
              f"Delete a task                  {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}gr.{RESET}  "
              f"Generate reports               {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}ds.{RESET}  "
              f"Display statistics             {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}e.{RESET}   "
              f"Exit the program               {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}╚══════════════════════════════════════"
              f"╝{RESET}")

        menu = input(f"{BOLD}Enter option:{RESET} ").strip().lower()

        if menu == 'r':
            register_new(user_manager)
        elif menu == 'a':
            add_task_input(task_manager, user_manager)
        elif menu == 'va':
            task_manager.view_all_tasks()
        elif menu == 'vm':
            view_user_tasks_input(task_manager,username)
        elif menu == 'vc':
            task_manager.view_completed_tasks()
        elif menu == 'del':
            delete_task_input(task_manager)
        elif menu == 'gr':
            report_gen.generate()
        elif menu == 'ds':
            report_gen.generate()
            report_gen.display_statistics()
        elif menu == 'e':
            print(f"\n{RED}Exiting program. Goodbye!{RESET}\n")
            break
        else:
            print(f"{RED}Invalid input. Please try again.{RESET}")


def user_menu(username, user_manager, task_manager):
    """
    Displays the user menu and handles user-specific actions.
    Uses styled and aligned output for a pleasant interface.
    """
    # ANSI escape codes for styling
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RED = "\033[31m"

    while True:
        print(f"\n{BOLD}{CYAN}╔════════════════════════════════════"
              f"══╗{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}    {BOLD}{GREEN}USER MENU OPTIONS"
              f"{RESET}                 {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}╠══════════════════════════════════════"
              f"╣{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}a.{RESET}   "
              f"Add a new task                 {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}va.{RESET}  "
              f"View all tasks                 {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}vm.{RESET}  "
              f"View user tasks                {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}  {GREEN}e.{RESET}   "
              f"Exit the program               {CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}╚══════════════════════════════════════"
              f"╝{RESET}")

        menu = input(f"{BOLD}Enter option:{RESET} ").strip().lower()

        # Execute corresponding function for selected option
        if menu == 'a':
            add_task_input(task_manager, user_manager)
        elif menu == 'va':
            task_manager.view_all_tasks()
        elif menu == 'vm':
            view_user_tasks_input(task_manager,username)
        elif menu == 'e':
            print(f"\n{RED}Exiting program. Goodbye!{RESET}\n")
            break
        else:
            print(f"{RED}Invalid input. Please try again.{RESET}")


def menu_options():
    user_manager = UserManager()
    task_manager = TaskManager()
    report_gen = ReportGenerator(task_manager, user_manager)

    username = input('\nPlease enter your username '
                  '(or type "e" to exit): ')
    if username.lower() == 'e':
            print("\nExiting login...")
            return None
    password = input('Please enter your password: ')

    if user_manager.authenticate(username, password):
        print(f"Welcome, {username}")
        if username == config["admin_username"]:
            admin_menu(username, user_manager, task_manager, report_gen)
        else:
            user_menu(username, user_manager, task_manager)
    else:
        print("Login failed.")


if __name__ == "__main__":
    menu_options()
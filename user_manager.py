"""
user_manager.py

Manages user data for the task manager app.

Classes:
- User: Stores username and password.
- UserManager: Loads, authenticates, adds, 
    and saves users from/to 'user.txt'.
"""
import os
import json

# Ensure the current directory is set correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("config.json", "r") as f:
    config = json.load(f)


class User:

    def __init__(self, username, password):
        # Assign the username and password to the object
        self.username = username
        self.password = password

    def __str__(self):
        # Returns a readable string representation of the user object
        return f"{self.username}, {self.password}"


class UserManager:

    def __init__(self, file_path=config["user_file"]):
        self.file_path = file_path
        self.users = []
        self.read_users()

    def read_users(self):
        """
        Reads users from 'user.txt' and loads them into self.users.
        Each line in the file is expected to be in the 
        format: username, password
        """
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    # Split line into username & password, and strip
                    fields = [f.strip() 
                              for f in line.strip().split(",")]
                    if len(fields) == 2:
                        username, password = fields
                        # Create a User and add it to the users list
                        self.users.append(User(username, password))
            return self.users
        except FileNotFoundError:
            # Handle missing file gracefully
            print("\nuser.txt file not found.")
            return None

    def authenticate(self, username, password):
        """
        Checks if the given credentials match any user in the system.
        Returns True if a match is found, else False.
        """
        return any(user.username == username and 
                   user.password == password for user in self.users)

    def save_users(self):
        """
        Saves the current user list to 'user.txt'.
        Overwrites the file with all current user data.
        """
        with open(self.file_path, "w") as f:
            for user in self.users:
                f.write(f"{user.username}, {user.password}\n")

    def add_user(self, user):
        """
        Adds a new User object to the system and saves it to the file.
        """
        self.users.append(user)
        self.save_users()
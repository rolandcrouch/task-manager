# Task Manager

A command-line Task Management System built with Python. It supports user registration, login authentication, task assignment, task tracking, and report generation. It uses plain text files for persistent storage and includes input validation and formatted CLI output.

## Features

- User login and authentication
- Register new users (admin only)
- Add, edit, view, and delete tasks
- View completed or user-specific tasks
- Generate detailed task and user overview reports
- Input validation helpers and reusable utilities
- Clean, styled terminal menus

## Project Structure

├── main.py # Entry point and menu system
├── task_manager_build.py # Task and TaskManager classes
├── user_manager.py # User and UserManager classes
├── user_input.py # Input validation and registration logic
├── report_generator.py # Reporting: task/user overviews
├── tasks.txt # Task storage
├── user.txt # User storage
├── task_overview.txt # Auto-generated task report
├── user_overview.txt # Auto-generated user report
├── requirements.txt # Dependencies
└── tests/ # Unit tests 

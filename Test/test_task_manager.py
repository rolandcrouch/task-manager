"""
test_task_manager.py

Unit tests for Task and TaskManager classes.

Covers task creation, string formatting, completion status,
and task management methods using mock file operations.
"""

import unittest
from unittest.mock import mock_open, patch
from task_manager_build import Task, TaskManager

# Test the Task class
class TestTask(unittest.TestCase):


    def test_task_str(self):
        """
        Test string representation of a Task.
        """
        task = Task("alice", "Test Task", "Do something", "01 Jan 2023", "05 Jan 2023")
        expected = ("User: alice\nTitle: Test Task\nDescription: Do something\n"
                    "Added: 01 Jan 2023\nDue: 05 Jan 2023\nCompleted: No")
        self.assertEqual(str(task), expected)


    def test_mark_complete(self):
        """
        Test marking a task as complete.
        """
        task = Task("bob", "Another Task", "Test description", "01 Jan 2023", "10 Jan 2023")
        task.mark_complete()
        self.assertEqual(task.completed, "Yes")


    def test_to_file_string(self):
        """
        Test converting task data to file string format.
        """
        task = Task("alice", "Test", "Something", "01 Jan 2023", "02 Jan 2023")
        expected = "alice, Test, Something, 01 Jan 2023, 02 Jan 2023, No"
        self.assertEqual(task.to_file_string(), expected)


# Test the TaskManager class
class TestTaskManager(unittest.TestCase):


    @patch("builtins.open", new_callable=mock_open, read_data="bob, Task1, Desc1, 01 Jan 2023, 05 Jan 2023, No\n")
    def test_load_tasks(self, mock_file):
        """
        Test loading tasks from file.
        """
        manager = TaskManager()
        self.assertEqual(len(manager.tasks), 1)
        self.assertEqual(manager.tasks[0].username, "bob")


    @patch("builtins.open", new_callable=mock_open)
    def test_add_task_and_save(self, mock_file):
        """
        Test adding a task and saving it to file.
        """
        manager = TaskManager()
        manager.tasks = []  # Ensure clean start
        task = Task("charlie", "Do Homework", "Math", "01 Jan 2023", "10 Jan 2023")
        manager.add_task(task)

        # Check if task was added to the internal list
        self.assertIn(task, manager.tasks)

        # Check if the task was written to the file
        mock_file().write.assert_called_with(task.to_file_string() + "\n")


    @patch("builtins.open", new_callable=mock_open)
    def test_delete_task(self, mock_file):
        """
        Test deleting a task by index and saving changes.
        """
        task1 = Task("user1", "T1", "D1", "01 Jan 2023", "02 Jan 2023")
        task2 = Task("user2", "T2", "D2", "01 Jan 2023", "03 Jan 2023")
        manager = TaskManager()
        manager.tasks = [task1, task2]
        manager.delete_task(0)  # Remove first task

        self.assertEqual(len(manager.tasks), 1)
        self.assertEqual(manager.tasks[0].title, "T2")


    def test_view_user_tasks(self):
        """
        Test viewing tasks for a specific user.
        """
        task1 = Task("alice", "Task A", "Test A", "01 Jan", "03 Jan")
        task2 = Task("bob", "Task B", "Test B", "01 Jan", "03 Jan")
        manager = TaskManager()
        manager.tasks = [task1, task2]

        # Patch print and check if bob's task gets printed
        with patch("builtins.print") as mock_print:
            manager.view_user_tasks("bob")
            mock_print.assert_any_call("User        : bob")


    def test_view_completed_tasks_none(self):
        """
        Test when no tasks are marked as completed.
        """
        manager = TaskManager()
        manager.tasks = [Task("x", "t", "d", "01", "02", "No")]

        # Should print that no completed tasks are found
        with patch("builtins.print") as mock_print:
            manager.view_completed_tasks()
            mock_print.assert_any_call("No completed tasks found.")


    def test_view_completed_tasks_some(self):
        """
        Test when some tasks are marked as completed.
        """
        t1 = Task("x", "t1", "d", "01", "02", "Yes")
        t2 = Task("y", "t2", "d", "01", "02", "No")
        manager = TaskManager()
        manager.tasks = [t1, t2]

        # Should display the completed task
        with patch("builtins.print") as mock_print:
            manager.view_completed_tasks()
            mock_print.assert_any_call("Completed   : Yes")


# Run the tests
if __name__ == '__main__':
    unittest.main()
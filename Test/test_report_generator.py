"""
test_report_generator.py

Unit tests for the ReportGenerator class which creates summary reports
about users and tasks. Uses mocking to simulate file I/O and filesystem behavior.
"""

import unittest
from unittest.mock import mock_open, patch
from report_generator import ReportGenerator
from task_manager_build import Task
from user_manager import User
import datetime


class TestReportGenerator(unittest.TestCase):


    def setUp(self):
        """
        Set up shared test data: two users and three tasks (1 overdue, 1 complete).
        """
        # Sample users
        self.users = [User("alice", "pass"), User("bob", "word")]

        # Sample tasks with different statuses and due dates
        self.tasks = [
            Task("alice", "Task 1", "Desc", "01 Jan 2023", "01 Jan 2022", "No"),  # Overdue
            Task("alice", "Task 2", "Desc", "01 Jan 2023", "01 Jan 2099", "No"),  # Future due
            Task("bob", "Task 3", "Desc", "01 Jan 2023", "01 Jan 2024", "Yes"),   # Completed
        ]

        # Create mock managers with task and user lists
        class MockTaskManager: tasks = self.tasks
        class MockUserManager: users = self.users

        # Initialize ReportGenerator with mock data
        self.report = ReportGenerator(MockTaskManager(), MockUserManager())


    @patch("builtins.open", new_callable=mock_open)
    def test_write_task_overview(self, mock_file):
        """
        Verify that write_task_overview writes the correct statistics.
        """
        self.report.write_task_overview()
        mock_file.assert_called_once_with("task_overview.txt", "w")

        # Get all written content
        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)

        self.assertIn("Total number of tasks             : 3", written)
        self.assertIn("Total number of completed tasks   : 1", written)
        self.assertIn("Total number of overdue tasks     : 1", written)


    @patch("builtins.open", new_callable=mock_open)
    def test_write_user_overview(self, mock_file):
        """
        Test that user statistics are written for each user.
        """
        self.report.write_user_overview()
        mock_file.assert_called_once_with("user_overview.txt", "w")

        handle = mock_file()
        content = "".join(call.args[0] for call in handle.write.call_args_list)

        self.assertIn("User: alice", content)
        self.assertIn("User: bob", content)
        self.assertIn("Tasks assigned", content)


    @patch("builtins.open", new_callable=mock_open)
    def test_generate_calls_both_reports(self, mock_file):
        """
        Ensure generate() calls both report writing methods.
        """
        with patch.object(self.report, "write_task_overview") as mock_task, \
             patch.object(self.report, "write_user_overview") as mock_user:
            self.report.generate()
            mock_task.assert_called_once()
            mock_user.assert_called_once()


    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    def test_display_statistics_generates_if_missing(self, mock_file, mock_exists):
        """
        If report files are missing, generate() should be called.
        """
        with patch.object(self.report, "generate") as mock_gen:
            self.report.display_statistics()
            mock_gen.assert_called_once()


    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="Fake content")
    def test_display_statistics_prints_files(self, mock_file, mock_exists):
        """
        If reports exist, display_statistics() should print their contents.
        """
        with patch("builtins.print") as mock_print:
            self.report.display_statistics()
            self.assertIn(
                unittest.mock.call("Fake content"),
                mock_print.mock_calls
            )


# Run the tests
if __name__ == '__main__':
    unittest.main()
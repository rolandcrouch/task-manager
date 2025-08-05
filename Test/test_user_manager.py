"""
test_user_manager.py

Unit tests for the User and UserManager classes.

Covers user creation, authentication, reading, saving, and adding users using mock file operations.
"""

import unittest
from unittest.mock import mock_open, patch
from user_manager import User, UserManager


class TestUser(unittest.TestCase):
    
    
    def test_user_str(self):
        """
        Test the string representation of a User object.
        """
        user = User("alice", "password123")
        self.assertEqual(str(user), "alice, password123")


class TestUserManager(unittest.TestCase):
    
    
    def setUp(self):
        """
        Prepare reusable mock data for multiple tests.
        """
        self.mock_users_data = "alice, password123\nbob, qwerty\n"
        self.mock_open = mock_open(read_data=self.mock_users_data)

    
    @patch("builtins.open", new_callable=mock_open, read_data="alice, password123\n")
    def test_read_users(self, mock_file):
        """
        Test that users are correctly read from user.txt.
        """
        manager = UserManager()
        self.assertEqual(len(manager.users), 1)
        self.assertEqual(manager.users[0].username, "alice")


    def test_authenticate_success(self):
        """
        Test successful authentication with correct credentials.
        """
        manager = UserManager()
        manager.users = [User("bob", "qwerty")]
        self.assertTrue(manager.authenticate("bob", "qwerty"))


    def test_authenticate_failure(self):
        """
        Test failed authentication with incorrect password.
        """
        manager = UserManager()
        manager.users = [User("bob", "qwerty")]
        self.assertFalse(manager.authenticate("bob", "wrongpass"))


    @patch("builtins.open", new_callable=mock_open)
    def test_save_users(self, mock_file):
        """
        Test that all users are correctly saved to user.txt.
        """
        manager = UserManager()
        manager.users = [User("alice", "123"), User("bob", "456")]
        manager.save_users()
        mock_file().write.assert_any_call("alice, 123\n")
        mock_file().write.assert_any_call("bob, 456\n")


    @patch("builtins.open", new_callable=mock_open)
    def test_add_user(self, mock_file):
        """
        Test that a new user is added and saved to user.txt.
        """
        manager = UserManager()
        manager.users = []
        new_user = User("charlie", "789")
        manager.add_user(new_user)
        self.assertIn(new_user, manager.users)
        mock_file().write.assert_called_with("charlie, 789\n")


if __name__ == '__main__':
    unittest.main()
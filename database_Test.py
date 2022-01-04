""" Test file for 'database.py' """
import unittest
import database


class TestDatabase(unittest.TestCase):
    def test_validateName(self):
        """ Test script for 'validateName(input)' """
        self.assertFalse(database.validateName("123"), "Name must be letters-only.")
        self.assertTrue(database.validateName("Din"), "Name should be valid.")
        self.assertTrue(database.validateName("Dean"), "Name should be valid.")
        self.assertTrue(database.validateName("Tali"), "Name should be valid.")
        self.assertTrue(database.validateName("Mendi"), "Name should be valid.")
        self.assertFalse(database.validateName("dsf#$"), "Name must be letters-only.")
        self.assertFalse(database.validateName("dsf333"), "Name must be letters-only.")

    def test_validateId(self):
        """ Test script for 'validateName(input)' """
        self.assertFalse(database.validateId("1r23"), "Name must be letters-only.")
        self.assertTrue(database.validateId("4234234"), "Name should be valid.")
        self.assertTrue(database.validateId("5544"), "Name should be valid.")
        self.assertTrue(database.validateId("00000"), "Name should be valid.")
        self.assertTrue(database.validateId("208273094"), "Name should be valid.")

    def test_validateAccountType(self):
        """ Test script for 'validateAccountType(input)' """
        self.assertFalse(database.validateAccountType("aabccd"), "Type should be invalid.")
        self.assertTrue(database.validateAccountType("Parent"), "Type should be valid.")
        self.assertTrue(database.validateAccountType("Child"), "Type should be valid.")
        self.assertTrue(database.validateAccountType("Tutor"), "Type should be valid.")
        self.assertFalse(database.validateAccountType("LALALA"), "Type should be invalid.")

    def test_isIdExists(self):
        """ Test script for 'isIdExists(idSearch)'
        This script is also testing the functions 'addUser' and 'deleteUser'. """
        idToTest = "9999999999"  # Fake ID example

        self.assertFalse(database.isIdExists(idToTest), "This user shouldn't exist yet.")

        # Add the user with the fake ID and test again
        database.addUser("fake", "fake", idToTest, "fake", "fake")
        self.assertTrue(database.isIdExists(idToTest), "This user should exist now.")

        # Delete the user and test again
        database.deleteUser(idToTest)
        self.assertFalse(database.isIdExists(idToTest), "This user was deleted, shouldn't exist anymore.")

    def test_validateLogin(self):
        """ Test script for 'validateLogin(idSearch)' """
        idToTest = "9999999999"  # Fake ID example
        goodPassword = "good"
        badPassword = "bad"

        # Add the user
        database.addUser("fake", "fake", idToTest, goodPassword, "fake")

        # Apply the tests
        self.assertFalse(database.validateLogin(idToTest, badPassword), "Input is invalid, should be false.")
        self.assertTrue(database.validateLogin(idToTest, goodPassword), "Input is valid, should be true.")

        # Delete the user
        database.deleteUser(idToTest)


if __name__ == '__main__':
    unittest.main()

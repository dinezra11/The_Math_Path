""" Test file for 'database.py' """
import unittest
import database


class TestTicTacToe(unittest.TestCase):
    def test_validateName(self):
        """ Test script for 'validateName(str)' """
        self.assertFalse(database.validateName("123"), "Name must be letters-only.")
        self.assertTrue(database.validateName("Din"), "Name should be valid.")
        self.assertTrue(database.validateName("Dean"), "Name should be valid.")
        self.assertTrue(database.validateName("Tali"), "Name should be valid.")
        self.assertTrue(database.validateName("Mendi"), "Name should be valid.")
        self.assertFalse(database.validateName("dsf#$"), "Name must be letters-only.")
        self.assertFalse(database.validateName("dsf333"), "Name must be letters-only.")

    def test_validateId(self):
        """ Test script for 'validateName(str)' """
        self.assertFalse(database.validateId("1r23"), "Name must be letters-only.")
        self.assertTrue(database.validateId("4234234"), "Name should be valid.")
        self.assertTrue(database.validateId("5544"), "Name should be valid.")
        self.assertTrue(database.validateId("00000"), "Name should be valid.")
        self.assertTrue(database.validateId("208273094"), "Name should be valid.")


if __name__ == '__main__':
    unittest.main()

import unittest
from financeTracker.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='animal')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='animal')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verificaton(self):
        u = User(password='animal')
        self.assertTrue(u.verify_password('animal'))
        self.assertFalse(u.verify_password('food'))

    def test_password_salts_are_random(self):
        u = User(password='animal')
        u2 = User(password='animal')
        self.assertTrue(u.password_hash != u2.password_hash)

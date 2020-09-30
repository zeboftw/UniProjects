import unittest
from Entities.class_Rental import Rental
from _datetime import date
from Entities.class_CustomError import CustomError
class TestRental(unittest.TestCase):
        
    def test_eq(self):
        with self.assertRaises(CustomError):
            Rental(10, 1, 1, date.today(), date.today()) == 10
        self.assertEqual(Rental(10, 1, 1, date.today(), date.today()), Rental(10, 100, 100, date.today(), date.today()))
        
    def test_str(self):
        self.assertEqual(str(Rental(10, 1, 1, date.today(), date.today())), 'Rental #10: Book #1 rented by client #1 at {} and returned at {}'.format(date.today(), date.today()))
        
    def test_set_return_date(self):
        new_rental = Rental(10, 1, 1, date.today(), None)
        new_rental.set_return_date(date.today())
        self.assertEqual(date.today(), new_rental.get_return_date())
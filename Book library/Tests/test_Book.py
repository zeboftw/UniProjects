import unittest
from Entities.class_Book import Book
from Entities.class_CustomError import CustomError
class TestBook(unittest.TestCase):
    
    def test_create_book(self):
        new_book = Book(10, 'test', 'book')
        self.assertEqual(new_book.get_id(), 10, 'book constructor failed')
        self.assertEqual(new_book.get_title(), 'test', 'book constructor failed')
        self.assertEqual(new_book.get_author(), 'book', 'book constructor failed')
        
    def test_str_on_book(self):
        new_book = Book(10, 'test', 'book')
        self.assertEqual(str(new_book), 'Book 10: test by book', 'str operation not working properly')
        
    def test_eq_on_book(self):
        book1 = Book(10, 'test', 'book')
        book1_same = Book(10, 'should', 'be equal')
        
        self.assertEqual(book1, book1_same, '== operator not working properly on books')
        
        book2 = Book(20, 'different', 'book')
        self.assertNotEqual(book1, book2, '== operator not recognizing different books')
        
        with self.assertRaises(CustomError):
            book1 == 10
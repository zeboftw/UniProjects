import unittest
from Entities.class_Book import Book
from Entities.class_Repository import Repository
from Entities.class_CustomError import CustomError
class TestRepository(unittest.TestCase):
    
    def setUp(self):
        self.repo = Repository(Book)
        self.book1 = Book(0, 'first', 'book')
        self.book1_copy = Book(0, 'copy', 'first')
        self.book2 = Book(10, 'different', 'book')
    
    def test_remove(self):
        self.repo.add(self.book1)
        self.assertRaises(CustomError, self.repo.remove, 10)
        self.assertRaises(CustomError, self.repo.remove, self.book2)
    
    def test_getitem(self):
        with self.assertRaises(CustomError):
            self.repo['zece']
        
    def test_add(self):
            
        self.repo.add(self.book2)
        self.assertEqual(len(self.repo), 1, 'add did not add element!')
        
        self.repo.add(self.book1)
        self.assertEqual(len(self.repo), 2, 'add did not add element!')
    
        self.assertRaises(CustomError, self.repo.add, 3)
        
        try:
            self.repo.add(self.book1_copy)
        except CustomError as ex:
            self.assertEqual(str(ex), "element already in repository!", 'repo does not raise exception for id conflict!')
        
        try:
            self.repo.add(self.book1_copy)
        except CustomError as ex:
            self.assertEqual(str(ex), "element already in repository!", 'repo does not raise exception for id conflict!')
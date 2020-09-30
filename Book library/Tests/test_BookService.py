import unittest
from Entities.class_Repository import Repository
from Entities.class_Book import Book
from Services.class_BookService import BookService
from Entities.class_Validator import BookValidator
from Entities.class_CustomError import CustomError
from Entities.class_UndoStack import UndoStack

class TestBookService(unittest.TestCase):
    
    def setUp(self):
        self.book_repo = Repository(Book)
        self.book_validator = BookValidator()
        self.undo_stack = UndoStack()
        self.book_service = BookService(self.book_repo, self.book_validator, self.undo_stack)
        self.book1 = Book(10, 'title', 'author')
        self.book1_copy = Book(10, 'copie', 'nu mere')
        self.book2 = Book(2, 'carte', 'diferita')
        
    def test_book_add(self):
        self.book_service.add_new_book(1, 'test', 'nou')
        self.assertEqual(1, len(self.book_repo))
        self.assertRaises(CustomError, self.book_service.add_new_book, 2.3, 'test', 'bou')
        self.assertRaises(CustomError, self.book_service.add_new_book, 1, '', 'bou')
        self.assertRaises(CustomError, self.book_service.add_new_book, 1, 'test', '')
        
    #===========================================================================
    # def test_book_remove(self):
    #     self.book_service.add_new_book(1, 'good', 'book')
    #     self.book_service.remove_book(1)
    #     self.assertEqual(0, len(self.book_repo))
    #     self.assertRaises(CustomError, self.book_service.remove_book, 22)
    #     self.assertRaises(CustomError, self.book_repo.remove, 22)
    #===========================================================================
        
    def test_update(self):
        self.book_service.add_new_book(10, 'test corect', 'corect')
        self.book_service.update_book(10, 'new name', 'new author')
        
        self.assertEqual(self.book_repo[10], Book(10, 'test equal', 'irelevant'))
        self.assertRaises(CustomError, self.book_service.update_book, 20, 'inexistent book', 'irelevant')
        
    def test_list(self):
        self.book_service.add_new_book(10, 'test corect', 'corect')
        self.book_service.add_new_book(11, 'test corect', 'corect')
        self.book_service.add_new_book(12, 'test corect', 'corect')
        counter = 0
        for x in self.book_service.list_all():
            counter+=1
        self.assertEqual(counter, 3)
        
    def test_search(self):
        self.book_service.add_new_book(10, 'copie apare', 'author')
        self.book_service.add_new_book(11, 'test apare', 'author')
        self.book_service.add_new_book(12, 'nu este returnat in search', 'author')
        
        counter = 0
        for book in self.book_service.search_book('id', 10):
            self.assertEqual(book.get_title(), 'copie apare', 'does not return correct item')
            counter+=1
        self.assertEqual(counter, 1, 'wrong number of returned elements')
        
        counter = 0
        for book in self.book_service.search_book('title', 'apare'):
            counter+=1
        self.assertEqual(2, counter, 'wrong number of returned elements')
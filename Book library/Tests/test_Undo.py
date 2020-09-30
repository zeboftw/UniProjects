import unittest
from Entities.class_Book import Book
from Entities.class_Validator import BookValidator, ClientValidator,RentalValidator
from Entities.class_Client import Client
from Entities.class_Repository import Repository
from Entities.class_Rental import Rental
from Entities.class_UndoStack import UndoStack
from Services.class_RentalService import RentalService
from Services.class_UndoService import UndoService
from Entities.class_CustomError import CustomError

class TestUndo(unittest.TestCase):
        
    def setUp(self):
        self.book_repo = Repository(Book)
        book_validator = BookValidator()
        self.client_repo = Repository(Client)
        client_validator = ClientValidator()
        self.rental_repo = Repository(Rental)
        rental_validator = RentalValidator()
        undo_stack = UndoStack()
        
        self.rental_service = RentalService(self.book_repo, book_validator, self.client_repo, client_validator, self.rental_repo, rental_validator, undo_stack)
        self.undo_service = UndoService(undo_stack)
        self.book1 = Book(1, 'test', 'book')
        self.book2 = Book(2, 'test 2', 'book')
        self.client1 = Client(1, 'test client')
        self.client2 = Client(2, 'nou client')
    
    def test_undo(self):
        self.book_repo.add(self.book1)
        self.client_repo.add(self.client1)
        self.book_repo.add(self.book2)
        self.client_repo.add(self.client2)
        self.rental_service.rent(1, 1, 1, 2019, 10, 10)
        self.rental_service.rent(2, 2, 1, 2019, 10, 10)
        self.rental_service.return_book(1)
        self.rental_service.return_book(2)
        
        self.rental_service.remove_book_and_rentals(1)
        self.assertEqual(len(self.rental_repo), 1)
        self.assertEqual(len(self.book_repo), 1)
        self.undo_service.undo()
        self.assertEqual(len(self.rental_repo), 2)
        self.assertEqual(len(self.book_repo), 2)
        self.undo_service.redo()
        self.assertRaises(CustomError, self.undo_service.redo)
        self.assertEqual(len(self.rental_repo), 1)
        self.assertEqual(len(self.book_repo), 1)
        
        self.undo_service.undo()
        self.rental_service.remove_book_and_rentals(1)
        self.assertRaises(CustomError, self.undo_service.redo)
        
        self.undo_service.undo()
        self.undo_service.undo()
        self.undo_service.undo()
        self.undo_service.undo()
        self.undo_service.undo()
        self.assertRaises(CustomError, self.undo_service.undo)
        
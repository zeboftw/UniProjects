import unittest
from Entities.class_Repository import Repository
from Entities.class_Book import Book
from Entities.class_Client import Client
from Entities.class_UndoStack import UndoStack
from Entities.class_Rental import Rental
from Services.class_RentalService import RentalService
from Entities.class_Validator import BookValidator, ClientValidator,RentalValidator
from _datetime import date
from Entities.class_CustomError import CustomError
class TestRentalService(unittest.TestCase):
    
    def setUp(self):
        self.book_repo = Repository(Book)
        book_validator = BookValidator()
        self.client_repo = Repository(Client)
        client_validator = ClientValidator()
        self.rental_repo = Repository(Rental)
        rental_validator = RentalValidator()
        undo_stack = UndoStack()
        
        self.rental_service = RentalService(self.book_repo, book_validator, self.client_repo, client_validator, self.rental_repo, rental_validator, undo_stack)
        self.book1 = Book(1, 'test', 'book')
        self.book2 = Book(2, 'test 2', 'book')
        self.client1 = Client(1, 'test client')
        self.client2 = Client(2, 'nou client')
        
    def test_rent_book(self):
        self.book_repo.add(self.book1)
        self.client_repo.add(self.client1)
        self.rental_service.rent(1, 1, 1, 2019, 10, 10)
        
        self.assertEqual(1, len(self.rental_repo), 'rental not added')
        self.assertIs(self.rental_repo[1].get_return_date(), None, 'returned date is set when it should be None')
        
        self.assertRaises(CustomError, self.rental_service.rent, 2, 1, 1, 2019, 10, 10)
        self.assertRaises(CustomError, self.rental_service.rent, 2, 10, 1, 2019, 10, 10)
        self.assertRaises(CustomError, self.rental_service.rent, 2, 1, 10, 2019, 10, 10)
        self.assertRaises(CustomError, self.rental_service.rent, 2, 1, 1, -1, 10, 10)
        
        self.rental_service.return_book(1)
        
        self.assertEqual(1, len(self.rental_repo), 'rental not added')
        self.assertEqual(self.rental_repo[1].get_return_date(), date.today(), 'returned date is set when it should be None')
        self.assertRaises(CustomError, self.rental_service.return_book, 1)
        
    def test_remove_book(self):
        self.book_repo.add(self.book1)
        self.client_repo.add(self.client1)
        self.rental_service.rent(1, 1, 1, 2019, 10, 10)
        
        self.rental_service.remove_book_and_rentals(1)
        self.assertEqual(0, len(self.book_repo))
        self.assertEqual(0, len(self.rental_repo))
        
    
    def test_remove_client(self):
        self.book_repo.add(self.book1)
        self.client_repo.add(self.client1)
        self.rental_service.rent(1, 1, 1, 2019, 10, 10)
        
        self.rental_service.remove_client_and_rentals(1)
        self.assertEqual(0, len(self.client_repo))
        self.assertEqual(0, len(self.rental_repo))
        
    def test_list_all(self):
        self.book_repo.add(self.book1)
        self.client_repo.add(self.client1)
        self.book_repo.add(self.book2)
        self.client_repo.add(self.client2)
        self.book_repo.add(Book(3, 'different book', 'different author'))
        self.rental_service.rent(1, 1, 1, 2019, 10, 10)
        self.rental_service.return_book(1)
        self.rental_service.rent(2, 1, 2, 2019, 1, 1)
        self.rental_service.return_book(1)
        self.rental_service.rent(3, 3, 2, 2019, 1, 1)
        self.rental_service.return_book(3)
        
        counter = 0
        for rental in self.rental_service.list_all():
            counter += 1
        self.assertEqual(3, counter)
        
    def test_top(self):
        self.book_repo.add(self.book1)
        self.client_repo.add(self.client1)
        self.book_repo.add(self.book2)
        self.client_repo.add(self.client2)
        self.book_repo.add(Book(3, 'different book', 'different author'))
        self.rental_service.rent(1, 1, 1, 2019, 10, 10)
        self.rental_service.return_book(1)
        self.rental_service.rent(2, 1, 2, 2019, 1, 1)
        self.rental_service.return_book(1)
        self.rental_service.rent(3, 3, 2, 2019, 1, 1)
        self.rental_service.return_book(3)
        
        last_author = None
        for author in self.rental_service.top('author'):
            last_author = author
        self.assertEqual(last_author, 'different author', 'top author does not return the right order of authors!')
        last_book = None
        for book in self.rental_service.top('book'):
            last_book = book
        self.assertEqual(last_book, Book(3, 'different book', 'different author'), 'top book error')
        last_client = None
        for client in self.rental_service.top('client'):
            last_client = client
        self.assertEqual(last_client, self.client1, 'top client error')
        
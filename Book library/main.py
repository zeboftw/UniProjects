#Linii de cod efective fara GUI 911
#GUI 348 linii de cod

from Services.class_BookService import BookService
from Services.class_ClientService import ClientService
from Services.class_RentalService import RentalService
from Services.class_UndoService import UndoService
from Entities.class_Repository import Repository
from Entities.class_Book import Book
from Entities.class_Client import Client
from Entities.class_Rental import Rental
from Entities.class_Validator import BookValidator, ClientValidator, RentalValidator
from Entities.class_UndoStack import UndoStack
from class_UI import UI
import unittest
from Tests.test_Book import TestBook
from Tests.test_Client import TestClient
from Tests.test_Rental import TestRental
from Tests.test_Repository import TestRepository
from Tests.test_BookService import TestBookService
from Tests.test_ClientService import TestClientService
from Tests.test_RentalService import TestRentalService
from Tests.test_Undo import TestUndo
import random
from GUI import GUI

if __name__ == '__main__':
    book_repo = Repository(Book)
    client_repo = Repository(Client)
    rental_repo = Repository(Rental)
    undo_stack = UndoStack()
    
    book_validator = BookValidator()
    client_validator = ClientValidator()
    rental_validator = RentalValidator()
    
    random_book_list = ['Harap Alb', '1Q89', '1984', 'Robinson Crusoe', 'Rokka no yuusha', 'All the lights we cannot see', "The anarchist's cookbook", 'Battle Royale', 'Overlord', 'The empty box and zeroth Maria', 'Youjo Senki', 'The magus', 'South of the border, west of the sun', 'Norwegian Woods']
    random_author_list = ['Ion Creanga', 'Haruki Murakami', 'George Orwell', 'Daniel Defoe', 'Anthony Doerr', 'Eiji Mikage', 'Carlo Zen']
    random_cient_list = ['Stefan', 'Gigi', 'Cristi', 'Ilinca', 'Mihaiela', 'Titi', 'Ion Luca Caragiale', 'Ion Luca', 'Ion', 'Corin', 'Ana', 'Viorica', 'Georgi']
    
    book_service = BookService(book_repo, book_validator, undo_stack)
    book_service.add_new_book(1, 'Robinson Crusoe', 'Danie Defoe')
    book_service.add_new_book(2, 'Robinson Copiat', 'Danie Defoe')
    book_service.add_new_book(3, 'Robinson nu mai e Crusoe', 'Harap Alb')
    client_service = ClientService(client_repo, client_validator, undo_stack)
    client_service.add_new_client(1, 'Adi')
    client_service.add_new_client(2, 'Dani')
    rental_service = RentalService(book_repo, book_validator, client_repo, client_validator, rental_repo, rental_validator, undo_stack)
    rental_service.rent(1, 1, 1, 2019, 10, 10)
    rental_service.return_book(1)
    rental_service.rent(2, 1, 2, 2018, 10, 10)
    rental_service.return_book(1)
    undo_service = UndoService(undo_stack)
    
    counter = 0
    while counter < 10:
        try:
            random_id = random.randint(4,100)
            random_client = random.choice(random_cient_list)
            if random_id % 3 == 0:
                random_client += ' sufix'
            client_service.add_new_client(random_id, random_client)
            counter+=1
        except:
            pass
    
    counter = 0
    while counter < 10:
        try:
            random_id = random.randint(4, 100)
            random_title = random.choice(random_book_list)
            random_author = random.choice(random_author_list)
            if random_id % 3 == 0:
                random_title += ' sufix'
            if random_id % 4 == 0:
                random_author += ' sufix'
            book_service.add_new_book(random_id, random_title, random_author)
            counter+=1
        except:
            pass
        
    ui = UI(book_service, client_service, rental_service, undo_service)
    gui = GUI(book_service, client_service, rental_service, undo_service)
    
    ui.run()
    unittest.main()
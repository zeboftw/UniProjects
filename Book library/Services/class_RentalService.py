from Entities.class_Book import Book
from Entities.class_Validator import BookValidator, ClientValidator
from Entities.class_Client import Client
from Entities.class_Rental import Rental
from Entities.class_CustomError import CustomError
from Entities.class_Action import Action, ComplexAction
from datetime import date
from Entities.class_Repository import Repository
class RentalService(object):
    
    def __init__(self, book_repo, book_validator, client_repo, client_validator, rental_repo, rental_validator, undo_stack):
        self.__book_repo = book_repo
        self.__book_validator = book_validator
        self.__client_repo = client_repo
        self.__client_validator = client_validator
        self.__rental_repo = rental_repo
        self.__rental_validator = rental_validator
        self.__undo_stack = undo_stack
    
    def list_all(self):
        return self.__rental_repo.get_all()
    
    def remove_book_and_rentals(self, book_id):
        book_to_remove = self.__book_repo[book_id]
        rentals_to_remove = []
        
        for rental in self.__rental_repo.get_all():
            if book_to_remove.get_id() == rental.get_book_id():
                rentals_to_remove.append(rental)
        
        action = ComplexAction()
            
        for rental in rentals_to_remove:
            self.__rental_repo.remove(rental)
            new_action = Action(self.__rental_repo, Repository.add, Repository.remove, rental)
            action.add_action(new_action)
        self.__book_repo.remove(book_to_remove)
        new_action = Action(self.__book_repo, Repository.add, Repository.remove, book_to_remove)
        action.add_action(new_action)
        self.__undo_stack.add(action)
    
    def remove_client_and_rentals(self, client_id):
        client_to_remove = self.__client_repo[client_id]
        rentals_to_remove = []
        
        action = ComplexAction()
        new_action = Action(self.__client_repo, Repository.add, Repository.remove, client_to_remove)
        action.add_action(new_action)
        
        for rental in self.__rental_repo.get_all():
            if client_to_remove.get_id() == rental.get_client_id():
                rentals_to_remove.append(rental)
                new_action = Action(self.__rental_repo, Repository.add, Repository.remove, rental)
                action.add_action(new_action)
            
        for rental in rentals_to_remove:
            self.__rental_repo.remove(rental)
            
        self.__client_repo.remove(client_to_remove)
        self.__undo_stack.add(action)
    
    def rent(self, rental_id, book_id, client_id, date_year, date_month, date_day):
        try:
            self.__book_repo[book_id]
        except CustomError:
            raise CustomError('book not found!')
        
        try:
            self.__client_repo[client_id]
        except CustomError:
            raise CustomError('client not found!')
        
        rental_date = None
        try:
            rental_date = date(date_year, date_month, date_day)
        except:
            raise CustomError('not a valid date!')
        
        for rental in self.__rental_repo.get_all():
            if rental.get_book_id() == book_id and rental.get_return_date() is None:
                raise CustomError('book already rented!')
        
        new_rental = Rental(rental_id, book_id, client_id, rental_date, None)
        new_action = Action(self.__rental_repo, Repository.remove, Repository.add, new_rental)
        self.__undo_stack.add(new_action)
        self.__rental_repo.add(new_rental)
    
    def return_book(self, book_id):
        rental_to_update = None
        
        for rental in self.__rental_repo.get_all():
            if rental.get_book_id() == book_id and rental.get_return_date() is None:
                rental_to_update = rental
        if rental_to_update is None:
            raise CustomError('book is not rented!')
                
        old_rental = Rental(rental_to_update.get_id(), rental_to_update.get_book_id(), rental_to_update.get_client_id(), rental_to_update.get_rented_date(), None)
        rental_to_update = Rental(rental_to_update.get_id(), rental_to_update.get_book_id(), rental_to_update.get_client_id(), rental_to_update.get_rented_date(), date.today())
        
        action = ComplexAction()
        new_action = Action(self.__rental_repo, Repository.remove, Repository.add, rental_to_update)
        action.add_action(new_action)
        new_action = Action(self.__rental_repo, Repository.add, Repository.remove, old_rental)
        action.add_action(new_action)
        
        self.__undo_stack.add(action)
        self.__rental_repo.remove(rental_to_update)
        self.__rental_repo.add(rental_to_update)
        
    def top(self, element_type):
        appearance_list = {}
        dict_key = None
        amount_to_add = 0
        
        if element_type == 'author':
            dict_key = lambda a: Book.get_author(self.__book_repo[a.get_book_id()])
            amount_to_add = lambda a: 1
            represented_element = lambda author_name: author_name
        elif element_type == 'book':
            dict_key = lambda a: a.get_book_id()
            amount_to_add = lambda a: 1
            represented_element = lambda book_id: self.__book_repo[book_id]
        else:
            dict_key = lambda a: a.get_client_id()
            amount_to_add = lambda a: 0 if a.get_return_date() is None else (a.get_return_date() - a.get_rented_date()).days
            represented_element = lambda client_id: self.__client_repo[client_id]
            
        for rental in self.__rental_repo.get_all():
            key = dict_key(rental)
            amount = amount_to_add(rental)
            if key not in appearance_list:
                appearance_list[key] = 0
            appearance_list[key] += amount
        
        list_elements = []
        for key in appearance_list.keys():
            list_elements.append([key, appearance_list[key]])
            
        sorting_criteria = lambda transfer_object : transfer_object[1]
        
        list_elements.sort(reverse = True, key=sorting_criteria)
        
        for element in list_elements:
            yield represented_element(element[0])
        
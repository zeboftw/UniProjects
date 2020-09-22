from Entities.class_CustomError import CustomError
from Services.class_BookService import BookService
from Services.class_ClientService import ClientService
from Services.class_RentalService import RentalService

class UI(object):
    
    
    def __init__(self, book_service, client_service, rental_service, undo_service):
        self.__book_service = book_service
        self.__client_service = client_service
        self.__rental_service = rental_service
        self.__undo_service = undo_service

    
    def ui_add(self):
        element_type = input("Input type of the element you want to add: ")
        
        if element_type == 'book':
            book_id = input("Input the id of the book you want to add: ")
            try:
                book_id = int(str(book_id))
            except:
                raise CustomError('non integer id!')
            book_title = input("Input the title of the book you want to add: ")
            if book_title == '':
                raise CustomError('name cannot be empty!')
            book_author = input("Input the author of the book you want to add: ")
            if book_author == '':
                raise CustomError('author cannot be empty!')
            self.__book_service.add_new_book(book_id, book_title, book_author)
        elif element_type == 'client':
            client_id = input('Input the id of the client you want to add: ')
            try:
                client_id = int(str(client_id))
            except:
                raise CustomError('non integer id!')
            client_name = input('Input the name of the client you want to add: ')
            if client_name == '':
                raise CustomError('name cannot be empty!')
            self.__client_service.add_new_client(client_id, client_name)
        else:
            raise CustomError('type not recognized!')

    def ui_remove(self):
        element_type = input('Input the type of the element you want to remove: ')
        if element_type == 'book':
            book_id = input('Input the id of the book to remove: ')
            try:
                book_id = int(str(book_id))
            except:
                raise CustomError('non integer id!')
            self.__rental_service.remove_book_and_rentals(book_id)
        elif element_type == 'client':
            client_id = input('Input the id of client to remove: ')
            try:
                client_id = int(str(client_id))
            except:
                raise CustomError('non integer id!')
            self.__rental_service.remove_client_and_rentals(client_id)
        else:
            raise CustomError('type not recognized!')
        
    def ui_update(self):
        element_type = input('Input the type of the element you want to add: ')
        if element_type == 'book':
            book_id = input('Input the id of the book you want to update: ')
            try:
                book_id = int(str(book_id))
            except:
                raise CustomError('non integer id!')
            new_name = input('Input the new title of the book: ')
            new_author = input('Input the new author of the book: ')
            self.__book_service.update_book(book_id, new_name, new_author)
        elif element_type == 'client':
            client_id = input('Input the id of the client you want to update: ')
            try:
                client_id = int(str(client_id))
            except:
                raise CustomError('non integer id!')
            new_name = input('Input the updated name of the client: ')
            self.__book_service.update_client(client_id, new_name)
        else:
            raise CustomError('type not recognized!')
    

    def ui_list(self):
        element_type = input('Input the type of the elements you want to list: ')
        if element_type == 'book':
            for book in self.__book_service.list_all():
                print(str(book))
        elif element_type == 'client':
            for client in self.__client_service.list_all():
                print(str(client))
        elif element_type == 'rental':
            for rental in self.__rental_service.list_all():
                print(str(rental))
        else:
            raise CustomError('type not recognized!')
    
    

    def ui_rent(self):
        rental_id = input('Input rental id: ')
        book_id = input('Input id of the rented book: ')
        client_id = input('Input id the client who rented: ')
        date_year = input('Input the year of the date: ')
        date_month = input('Input the month of the date: ')
        date_day = input('Input the day of the date: ')
        
        try:
            rental_id = int(str(rental_id))
            book_id = int(str(book_id))
            client_id = int(str(client_id))
        except:
            raise CustomError('id is not an integer!')
        
        try:
            date_year = int(str(date_year))
            date_month = int(str(date_month))
            date_day = int(str(date_day))
        except:
            raise CustomError('not a valid date!')
        
        self.__rental_service.rent(rental_id, book_id, client_id, date_year, date_month, date_day)
    

    def ui_return(self):
        book_id = input('Input the id of the book you want to return: ')
        try:
            book_id = int(str(book_id))
        except:
            raise CustomError('id not an integer!')
        self.__rental_service.return_book(book_id)
    

    def ui_search(self):
        element_type = input('Input the type of the element you want to search for: ').lower()
        element_field = input('Input the field to search for: ').lower()
        search_term = input('Input the search term: ').lower()
        returned_elements = []
        
        if element_type == 'book':
            if element_field != 'title' and element_field != 'author' and element_field != 'id':
                raise CustomError('field not recognized!')
            
            if element_field == 'id':
                try:
                    search_term = int(str(search_term))
                except:
                    raise CustomError('cannot search by id with a non integer search term!')
                
            returned_elements = self.__book_service.search_book(element_field, search_term)
        elif element_type == 'client':
            if element_field != 'id' and element_field != 'name':
                raise CustomError('field not recognized!')
            
            if element_field == 'id':
                try:
                    search_term = int(str(search_term))
                except:
                    raise CustomError('cannot search by id with a non integer search term!')
            
            returned_elements = self.__client_service.search_client(element_field, search_term)
        else:
            raise CustomError('type not recognized!')
        
        for element in returned_elements:
            print(str(element))
        

    def ui_top(self):
        element_type = input('Input the type of the top: ').lower()
        returned_elements = []
        
        if element_type == 'book' or element_type == 'client' or element_type == 'author':
            returned_elements = self.__rental_service.top(element_type)
            for element in returned_elements:
                print(str(element))
        else:
            raise CustomError('type not recognized!')
    
    
    def ui_undo(self):
        self.__undo_service.undo()
    
    def ui_redo(self):
        self.__undo_service.redo()
    
    
    def run(self):
        while True:
            cmd = input(">>>")
        
            cmd_list = {
                'add':self.ui_add,
                'remove':self.ui_remove,
                'update':self.ui_update,
                'list':self.ui_list,
                'rent':self.ui_rent,
                'return':self.ui_return,
                'search':self.ui_search,
                'top':self.ui_top,
                'undo':self.ui_undo,
                'redo':self.ui_redo
                }
            
            if cmd == 'exit':
                break
            if cmd in cmd_list:
                try:
                    cmd_list[cmd]()
                except CustomError as ex:
                    print(str(ex))
            else:
                print("command not found!")
            
from Entities.class_Book import Book
from Entities.class_Validator import BookValidator
from Entities.class_Repository import Repository
from Entities.class_CustomError import CustomError
from Entities.class_Action import ComplexAction, Action

class BookService(object):
    
    
    def __init__(self, book_repo, book_validator, undo_stack):
        self.__book_repo = book_repo
        self.__book_validator = book_validator
        self.__undo_stack = undo_stack
    
    def add_new_book(self, book_id, book_title, book_author):
        book_to_add =  Book(book_id, book_title, book_author)
        self.__book_validator.book_validate(book_to_add)
        
        self.__book_repo.add(book_to_add)
        action = Action(self.__book_repo, Repository.remove, Repository.add, book_to_add)
        self.__undo_stack.add(action)
        
    #===========================================================================
    # def remove_book(self, book_id):
    #     book_to_remove = Book(book_id, 'irelevant', 'irelevant')
    #     self.__book_validator.book_validate(book_to_remove)
    #     self.__book_repo.remove(book_to_remove)
    #===========================================================================
        
    def update_book(self, book_id, book_name, book_author):
        book_to_update = Book(book_id, book_name, book_author)
        self.__book_validator.book_validate(book_to_update)
        
        if self.__book_repo.search(book_to_update):
            action = ComplexAction()
            new_action = Action(self.__book_repo, Repository.remove, Repository.add, book_to_update)
            action.add_action(new_action)
            new_action = Action(self.__book_repo, Repository.add, Repository.remove, self.__book_repo[book_id])
            action.add_action(new_action)
            
            self.__undo_stack.add(action)
            self.__book_repo.remove(book_to_update)
            self.__book_repo.add(book_to_update)
        else:
            raise CustomError('book does not exist!')
        
    def list_all(self):
        return self.__book_repo.get_all()
    
    def search_book(self, element_field, search_term):
        if element_field == 'id':
            yield self.__book_repo[search_term]
        else:
            for book in self.__book_repo.get_all():
                if (element_field == 'title' and search_term in book.get_title().lower()) or (element_field == 'author' and search_term in book.get_author().lower()):
                    yield book
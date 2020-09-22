from Entities.class_CustomError import CustomError

class Book(object):
    
    def __init__(self, book_id, book_title, book_author):
        self.__book_id = book_id
        self.__book_title = book_title
        self.__book_author = book_author
    
    def get_id(self):
        return self.__book_id
    
    def get_title(self):
        return self.__book_title
    
    def get_author(self):
        return self.__book_author

    def __eq__(self, other):
        if type(other) is not Book:
            raise CustomError('cannot compare type Book with anything but type Book!')
        
        return self.__book_id == other.get_id()
    
    def __str__(self):
        return "Book {}: {} by {}".format(self.__book_id, self.__book_title, self.__book_author)
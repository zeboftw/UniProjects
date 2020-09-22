from Entities.class_CustomError import CustomError
from Entities.class_Book import Book
from Entities.class_Client import Client

class ClientValidator(object):
    def client_validate(self, object_to_validate):
        if type(object_to_validate.get_id()) is not int:
            raise CustomError('created object client with a non integer id!')
        if object_to_validate.get_name() == '':
            raise CustomError('created object client with an empty title!')
    pass

class RentalValidator(object):
    pass

class BookValidator(object):
    def book_validate(self, object_to_validate):
        if type(object_to_validate.get_id()) is not int:
            raise CustomError('created object book with a non integer id!')
        if object_to_validate.get_title() == '':
            raise CustomError('created object book with empty name!')
        if object_to_validate.get_author() == '':
            raise CustomError('created object client with empty author!')
    pass



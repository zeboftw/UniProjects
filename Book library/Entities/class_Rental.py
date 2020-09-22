from Entities.class_CustomError import CustomError
class Rental(object):
    
    
    def __init__(self, rental_id, book_id, client_id, rental_date, return_date):
        self.__rental_id = rental_id
        self.__book_id = book_id
        self.__client_id = client_id
        self.__rental_date = rental_date
        self.__return_date = return_date
    
    def get_id(self):
        return self.__rental_id
    
    def get_book_id(self):    
        return self.__book_id
    
    def get_client_id(self):
        return self.__client_id
    
    def get_return_date(self):
        return self.__return_date
    
    def get_rental_id(self):
        return self.__rental_id
    
    def get_rented_date(self):
        return self.__rental_date
    
    def set_return_date(self, return_date):
        self.__return_date = return_date
        
    def __eq__(self, other):
        if type(other) is not Rental:
            raise CustomError('comparison between Rental object and non Rental object!')
        return other.get_rental_id() == self.__rental_id

    
    def __str__(self):
        return 'Rental #{}: Book #{} rented by client #{} at {} and returned at {}'.format(self.__rental_id, self.__book_id, self.__client_id, self.__rental_date, self.__return_date)




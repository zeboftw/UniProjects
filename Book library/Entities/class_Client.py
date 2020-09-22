from Entities.class_CustomError import CustomError
class Client(object):
    
    def __init__(self, client_id, client_name):
        self.__client_id = client_id
        self.__client_name = client_name
    
    def get_name(self):
        return self.__client_name
    
    def get_id(self):
        return self.__client_id
    
    def __eq__(self, other):
        if type(other) is not Client:
            raise CustomError('comparisson between different Client object and non Client object!')
        
        return other.get_id() == self.__client_id
    
    def __str__(self):
        return "Client #{}: {}".format(self.__client_id, self.__client_name)
    
    pass



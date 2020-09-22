from Entities.class_CustomError import CustomError

class Repository(object):
    
    
    def __init__(self, element_type):
        self.__element_type = element_type
        self.__list = []

    def search(self, element_to_search):
        for element in self.__list:
            if element == element_to_search:
                return True
        return False

    def add(self, element_to_add):
        if type(element_to_add) is not self.__element_type:
            raise CustomError("tried to add invalid type to repository!")
        
        if self.search(element_to_add):
            raise CustomError("element already in repository!")
            
        self.__list.append(element_to_add)
        
    def remove(self, element_to_remove):
        if type(element_to_remove) is not self.__element_type:
            raise CustomError("tried to remove invalid type to repository!")
        
        if not self.search(element_to_remove):
            raise CustomError("element not in repository!")
        
        self.__list.remove(element_to_remove)
        
    def get_all(self):
        return self.__list[:]
        
    def __getitem__(self, key):
        try:
            key = int(str(key))
        except:
            raise CustomError('key not an integer!')
        
        for x in self.__list:
            if x.get_id() == key:
                return x
        raise CustomError('element not found!')
        
    def __len__(self):
        return len(self.__list)
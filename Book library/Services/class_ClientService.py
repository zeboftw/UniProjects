from Entities.class_Client import Client
from Entities.class_Repository import Repository
from Entities.class_Validator import ClientValidator
from Entities.class_CustomError import CustomError
from Entities.class_Action import Action, ComplexAction

class ClientService(object):
    
    
    def __init__(self, client_repo, client_validator, undo_stack):
        self.__client_repo = client_repo
        self.__client_validator = client_validator
        self.__undo_stack = undo_stack
    
    def add_new_client(self, client_id, client_name):
        new_client = Client(client_id, client_name)
        self.__client_validator.client_validate(new_client)
        
        self.__client_repo.add(new_client)
        action = Action(self.__client_repo, Repository.remove, Repository.add, new_client)
        self.__undo_stack.add(action)
    
    #===========================================================================
    # def remove_client(self, client_id):
    #     client_to_remove = Client(client_id, 'irelevant')
    #     self.__client_validator.client_validate(client_to_remove)
    #     
    #     self.__client_repo.remove(client_to_remove)
    #===========================================================================
        
    def update_client(self, client_id, client_name):
        client_to_update = Client(client_id, client_name)
        self.__client_validator.client_validate(client_to_update)
        
        if self.__client_repo.search(client_to_update):
            action = ComplexAction()
            new_action = Action(self.__client_repo, Repository.add, Repository.remove, self.__client_repo[client_id])
            action.add_action(new_action)
            new_action = Action(self.__client_repo, Repository.remove, Repository.add, client_to_update)
            action.add_action(new_action)
            self.__undo_stack.add(action)
            
            self.__client_repo.remove(client_to_update)
            self.__client_repo.add(client_to_update)
        else:
            raise CustomError('client does not exist!')
        
    def list_all(self):
        return self.__client_repo.get_all()
    
    def search_client(self, element_field, search_term):
        if element_field == 'id':
            print ('looking for client with id: '+str(search_term))
            yield self.__client_repo[search_term]
        else:
            for client in self.__client_repo.get_all():
                if search_term in client.get_name().lower():
                    yield client
from Entities.class_Client import Client
from Services.class_ClientService import ClientService
import unittest
from Entities.class_Repository import Repository
from Entities.class_Validator import ClientValidator
from Entities.class_CustomError import CustomError
from Entities.class_UndoStack import UndoStack

class TestClientService(unittest.TestCase):
    
    def setUp(self):
        self.client_repo = Repository(Client)
        self.client_validator = ClientValidator()
        self.undo_stack = UndoStack()
        self.client_service = ClientService(self.client_repo, self.client_validator, self.undo_stack)
        
    def test_add(self):
        self.client_service.add_new_client(10, 'test corect')
        self.assertEqual(1, len(self.client_repo))
        
    #===========================================================================
    # def test_remove(self):
    #     self.client_service.add_new_client(10, 'test corect')
    #     self.client_service.remove_client(10)
    #     self.assertEqual(0, len(self.client_repo))
    #===========================================================================
        
    def test_update(self):
        self.client_service.add_new_client(10, 'test corect')
        self.client_service.update_client(10, 'new name')
        
        self.assertEqual(self.client_repo[10], Client(10, 'test equal'))
        self.assertRaises(CustomError, self.client_service.update_client, 20, 'inexistent client')
    
    def test_list(self):
        self.client_service.add_new_client(10, 'test corect')
        self.client_service.add_new_client(11, 'test corect')
        self.client_service.add_new_client(12, 'test corect')
        
        counter = 0
        for x in self.client_service.list_all():
            counter+=1
        self.assertEqual(counter, 3)
        
    def test_search(self):
        self.client_service.add_new_client(10, 'apare la search')
        self.client_service.add_new_client(11, 'si el apare')
        self.client_service.add_new_client(12, 'dar asta nu')
        
        for client in self.client_service.search_client('id', 10):
            self.assertEqual(client.get_name(), 'apare la search', 'returned wrong element')
            
        counter = 0
        for client in self.client_service.search_client('name', 'apare'):
            counter+=1
        self.assertEqual(counter, 2, 'does not return the expected amount of elements')
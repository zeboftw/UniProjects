import unittest
from Entities.class_Validator import ClientValidator
from Entities.class_CustomError import CustomError
from Entities.class_Client import Client

class TestClient(unittest.TestCase):
    
    def setUp(self):
        self.client_validator = ClientValidator()
    
    def test_valid(self):
        self.assertRaises(CustomError, self.client_validator.client_validate, Client('zece', ''))
        self.assertRaises(CustomError, self.client_validator.client_validate, Client(10, ''))
        pass
    
    def test_eq(self):
        with self.assertRaises(CustomError):
            Client(10, 'ilegal comparison') == 10
        self.assertEqual(Client(10, 'equals'), Client(10, 'just the id has to match'))
        
    def test_str(self):
        self.assertEqual(str(Client(10, 'Gigel')), 'Client #10: Gigel')
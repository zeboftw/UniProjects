import unittest
from Services.class_Service import Service
from Entities.class_CustomError import CustomError

class test_class_Service(unittest.TestCase):
    
    def setUp(self):
        self.service = Service()
        
    def test_place(self):
        self.service.place_at(0, 0, 5, 5, False)
        
        pc_table = self.service.debug_get_pc()
        
        self.assertEqual(1, pc_table[3][5], 'Ship not properly placed')
        
        self.assertRaises(CustomError, self.service.place_at, 0, 0, 3, 5, False)
        self.assertRaises(CustomError, self.service.place_at, 0, 0, -5, 3, False)
        self.assertRaises(CustomError, self.service.place_at, 0, 1, 7, 3, False)
        
    def test_hit(self):
        self.service.create_ai()
        
        self.assertRaises(CustomError, self.service.hit, -10, 10)
        self.assertRaises(CustomError, self.service.hit, 5, 10)
        
        try:
            self.service.place_at(2, 2, 4, 4, True)
        except CustomError:
            pass
        result = self.service.hit(4, 4)
        self.assertEqual(result[0], True, 'Correct hit did not register!')
        self.assertRaises(CustomError, self.service.hit, 4, 4)
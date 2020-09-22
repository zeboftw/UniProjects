import unittest
from Entities.class_AI import AI

class test_class_AI(unittest.TestCase):
    
    def setUp(self):
        self.ai = AI()
    
    def test_clear_map(self):
        self.ai._clear_heat_map()
        heat = self.ai.debug_get_heat()
        for row in heat:
            for value in row:
                self.assertEqual(0, value, 'Map not cleared!')
        pass
    
    def test_update(self):
        self.ai.update(3, 4, False)
        heat = self.ai.debug_get_heat()
        hit = self.ai.debug_get_hit()
        self.assertEqual(0, heat[3][4], 'Heat value wrong!')
        self.assertEqual(False, hit[3][4], 'Hit did not register!')
        
    def test_update_heat_map(self):
        self.ai.update(4, 4, False)
        heat = self.ai.debug_get_heat()
        self.assertEqual(18, heat[3][3], 'Heat did not compute correctly!')
        
    def test_request_target(self):
        target = self.ai.request_target(False)
        potential_targets = [3,3],[4,4],[3,4],[4,3]
        for potential_target in potential_targets:
            if target == potential_target:
                return
        assert(False)
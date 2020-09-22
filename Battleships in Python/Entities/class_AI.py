from random import randint
from copy import deepcopy
class AI():
    
    def _clear_heat_map(self):
        """
        Function that makes a new list for the __heat_map attribute containing 8 other lists, each having 8 elements, all = 0
        returns nothing
        """
        self.__heat_map = []
        for i in range(0, 8):
            row = []
            hit_row = []
            for j in range(0, 8):
                row.append(0)
            self.__heat_map.append(row)
    
    def __init__(self):
        self.__more_human = True
        self.__heat_map = []
        self.__hit_map = []
        
        self._clear_heat_map()
        
        for i in range(0, 8):
            hit_row = []
            for j in range(0, 8):
                hit_row.append(None)
            self.__hit_map.append(hit_row)
        
        self.update_heat_map()
    
    def update_heat_map(self):
        self._clear_heat_map()
        for length in range(2, 5):
            
            for i in range(0, 8):
                for j in range(0, 9-length):
                    value_to_add = 1
                    for x in range(0, length):
                        if self.__hit_map[i][j+x] == True:
                            value_to_add = 6-length
                        elif self.__hit_map[i][j+x] == False:
                            value_to_add = 0
                            break
                    for x in range(0, length):
                        self.__heat_map[i][j+x] += value_to_add
            
            for i in range(0, 9-length):
                for j in range(0, 8):
                    value_to_add = 1
                    
                    for x in range(0, length):
                        if self.__hit_map[i+x][j] == True:
                            value_to_add = 6-length
                        elif self.__hit_map[i+x][j] == False:
                            value_to_add = 0
                            break
                    for x in range(0, length):
                        self.__heat_map[i+x][j] += value_to_add
                        
        pass
    
    def update(self, x, y, hit):
        """
        Function that registers a hit or a miss in the AI's matrix
        x, y - integers
        hit - boolean
        returns nothing
        """
        self.__hit_map[x][y] = hit
        self.update_heat_map()
        pass
    
    def more_human(self, potentials, cmp_val):
        cmp_funct = lambda a: True if a>cmp_val-2 and a<cmp_val+2 and a!=cmp_val else False
        for x in range(0, 8):
            for y in range(0, 8):
                if cmp_funct(self.__heat_map[x][y]) and self.__hit_map[x][y] is None:
                    potentials.append([x,y])
    
    def request_target(self, is_min):
        """
        Function that searches through the heat_map and finds the most suitable target for the next attack
        is_min boolean
        returns a list of 2 integers
        """
        if self.__more_human:
            is_min = False
        compare_func = lambda a, b: True if a>=b else False
        compare_value = -1
        if is_min:
            compare_func = lambda a, b: True if a<=b else False
            compare_value = 0x0FFFFFFF
        
        potential_targets = []
        for i in range(0, 8):
            for j in range(0, 8):
                if compare_func(self.__heat_map[i][j], compare_value) and self.__hit_map[i][j] is None:
                    if compare_value == self.__heat_map[i][j]:
                        potential_targets.append([i,j])
                    else:
                        compare_value = self.__heat_map[i][j]
                        potential_targets = []
                        potential_targets.append([i,j])
                        if self.__more_human:
                            self.more_human(potential_targets, compare_value)
        
        print("Potential targets: " + str(len(potential_targets)))
        aux = randint(0, len(potential_targets)-1)
        
        return potential_targets[aux]
        
    
    def get_random_ship_location(self):
        """
        Function that generates a random direction and random coordinates for any type of ship
        returns a tuple
        """
        direction = randint(0,3)
        x = randint(0,7)
        y = randint(0,7)
        
        return direction,x,y
    
    def debug(self):
        msg = "=============Heat Table===========\n"
        for row in self.__heat_map:
            msg += str(row) + '\n'
        msg += "=============Hit Table===========\n"
        for row in self.__hit_map:
            msg += str(row) + '\n'
        
        return msg
    def debug_get_heat(self):
        """
        Getter for the purpose of debugging and testing
        returns a deepcopy of the heat_map
        """
        return deepcopy(self.__heat_map)
    
    def debug_get_hit(self):
        """
        Getter for the purpose of debugging and testing
        returns a deepcopy of the hit_map
        """
        return deepcopy(self.__hit_map)
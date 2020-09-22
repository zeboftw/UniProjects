from Entities.class_CustomError import CustomError
from Entities.class_AI import AI
from copy import deepcopy
class Service():
    
    def __init__(self):
        self.__pc_table = []
        self.__enemy_table = []
        self.__pc_lives = 9
        self.__enemy_lives = 9
        
        for i in range(8):
            pc_row = []
            enemy_row = []
            for j in range(8):
                pc_row.append(0)
                enemy_row.append(0)
            self.__pc_table.append(pc_row)
            self.__enemy_table.append(enemy_row)
        
        pass
    
    def hit(self, x, y):
        """
        Function that registers a PC hit and an AI hit and checks if the players are still alive
        x, y - integers
        returns a tuple(boolean, int, int, boolean)
        raises CustomError if the PC tried to hit at illegal coordinates
        """
        if self.__enemy_lives == 0:
            raise CustomError('You won!')
        if self.__pc_lives == 0:
            raise CustomError('You lost!')
        
        if x<0 or x>7:
            raise CustomError('coordinate x out of range')
        if y<0 or y>7:
            raise CustomError('coordinate y out of range')
        
        if self.__enemy_table[x][y] == -1:
            raise CustomError('already hit there')
        
        result = self.__enemy_table[x][y] == 1
        if result:
            self.__enemy_lives -= 1
        self.__enemy_table[x][y] = -1
        
        coordinates = self.__enemy.request_target(self.__is_min)
        coord_x = coordinates[0]
        coord_y = coordinates[1]
        enemy_result = self.__pc_table[coord_x][coord_y] == 1
        if enemy_result:
            self.__pc_lives -= 1
        self.__enemy.update(coord_x, coord_y, enemy_result)
        
        return result, coord_x, coord_y, enemy_result
        
    def create_ai(self):
        """
        Function that creates an enemy AI and places it's ships on the table
        returns nothing
        """
        self.__enemy = AI()
        self.__is_min = False
        
        for ship_type in range(0, 3):
            while(True):
                try:
                    target = self.__enemy.get_random_ship_location()
                    self.place_at(ship_type, target[0], target[1], target[2], True)
                    break
                except CustomError:
                    pass
                
        
    def place_at(self, ship_type, direction, x, y, is_enemy):
        """
        Function that verifies if a ship can fit at specified coordinates and updates the map in case it does
        ship_type, direction, x, y - integers
        is_enemy - boolean
        raises CustomError if the ship can't fit at specified coordinates
        returns nothing
        """
        target_board = self.__pc_table
        if is_enemy:
            target_board = self.__enemy_table
        length = 3-ship_type
        dir_x = 0
        dir_y = 0
        
        if direction == 0:
            dir_x = -1
        elif direction == 1:
            dir_x = 1
        elif direction == 2:
            dir_y = -1
        else:
            dir_y = 1
            
            
        #print("--------------------DEBUG----------------\nship_type={}\ndir_x={} dir_y={}\nlength={},x={} y={}".format(ship_type, dir_x, dir_y, length, x, y))
        
        if x < 0 or x > 7:
            raise CustomError('coordinate x out of border')
        if y < 0 or y > 7:
            raise CustomError('coordinate y out of border')
        
        if x + length*dir_x < 0 or x + length*dir_x > 7:
            raise CustomError('coordinate x out of border')
        if y + length*dir_y < 0 or y + length*dir_y > 7:
            raise CustomError('coordinate y out of border')
        
        for i in range(0, length+1):
            if target_board[x+i*dir_x][y+i*dir_y] == 1:
                raise CustomError('overlapping with other ship')
            
        for i in range(0, length+1):
            target_board[x+i*dir_x][y+i*dir_y] = 1
    
    def debug(self):
        msg = "===============YOUR TABLE =================\n"
        for row in self.__pc_table:
            msg += str(row)+'\n'
        msg += "==============Enemy Table===================\n"
        for row in self.__enemy_table:
            msg += str(row)+'\n'
        msg += self.__enemy.debug()
        return msg
        
    def debug_get_pc(self):
        """
        Getter for the purpose of debugging and testing
        returns a deepcopy of the pc_table
        """
        return deepcopy(self.__pc_table)
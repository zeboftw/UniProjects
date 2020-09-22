from Entities.class_CustomError import CustomError
class UI():
    
    def __init__(self, service):
        self.__service = service
        self.__pc_lives = 9
        self.__enemy_lives = 9
        
        self.__pc_table = []
        self.__enemy_talbe = []
        for i in range(0, 8):
            pc_row = []
            enemy_row = []
            for j in range(0, 8):
                pc_row.append('?')
                enemy_row.append('?')
            self.__pc_table.append(pc_row)
            self.__enemy_talbe.append(enemy_row)
        
    def print_tables(self):
        print("=========== YOUR TABLE ==============")
        for row in self.__pc_table:
            print(str(row))
        print("=========== ENEMY TABLE =============")
        for row in self.__enemy_talbe:
            print(str(row))
    
    def place_pc_ships(self):
        for ship in range(0, 3):
            while True:
                ships = ["Battleship", "Destroyer", "Cruiser"]
                direction = input('Input direction of the tip of the {}\n0 - South\n1 - North\n2 - East\n3 - West'.format(ships[ship]))
                try:
                    direction = int(str(direction))
                except:
                    print('Not a valid input')
                    continue
                if direction not in [0,1,2,3]:
                    print('Not a valid input')
                    continue
                
                coord_x = input('Input the row:')
                coord_y = input('Input the column:')
                try:
                    coord_x = int(str(coord_x))
                    coord_y = int(str(coord_y))
                    assert(coord_x>=0)
                    assert(coord_y>=0)
                    assert(coord_x<8)
                    assert(coord_y<8)
                except:
                    print("Not a valid input")
                    continue
                
                try:
                    self.__service.place_at(ship, direction, coord_x, coord_y, False)
                except CustomError as ex:
                    print(str(ex))
                    continue
                
                length = 4-ship
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
                    
                for i in range(0, length):
                    coord_i = coord_x + i*dir_x
                    coord_j = coord_y + i*dir_y
                    self.__pc_table[coord_i][coord_j] = '~'
                break
    
    def battle(self):
        while self.__pc_lives > 0 and self.__enemy_lives > 0:
            self.print_tables()
            
            print("Input the coordinates of the atack: ")
            coord_x = input('Input the row:')
            coord_y = input('Input the column:')
            try:
                coord_x = int(str(coord_x))
                coord_y = int(str(coord_y))
                assert(coord_x>=0)
                assert(coord_y>=0)
                assert(coord_x<8)
                assert(coord_y<8)
            except:
                print("Not a valid input")
                continue
            
            result = None
            try:
                result = self.__service.hit(coord_x, coord_y)
            except CustomError as ex:
                print(str(ex))
                continue
            
            if result[0]:
                self.__enemy_lives-=1
                self.__enemy_talbe[coord_x][coord_y] = 'x'
            else:
                self.__enemy_talbe[coord_x][coord_y] = '0'
                
            coord_x = result[1]
            coord_y = result[2]
            if result[3]:
                self.__pc_lives-=1
                self.__pc_table[coord_x][coord_y] = 'x'
            else:
                self.__pc_table[coord_x][coord_y] = '0'
        
        self.print_tables()
        if self.__pc_lives == 0:
            print ('You lose!')
        else:
            print("You win!")
    
    def run(self):
        self.place_pc_ships()
        self.__service.create_ai()
        self.battle()
                
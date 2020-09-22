import tkinter as tk
from tkinter import ttk, messagebox
from Entities.class_CustomError import CustomError

class TableGrid(tk.Canvas):
    
    def __init__(self, master):
        tk.Canvas.__init__(self, master, width=8*40+150+8*40, height=8*40+20)
        self.__pc_grid = []
        self.__enemy_grid = []
        for i in range(0,8):
            pc_row = []
            for j in range(0,8):
                square = self.create_rectangle(50+j*40, 10+i*40, 50+(j+1)*40, 10+(i+1)*40, fill='blue')
                pc_row.append(square)
            self.__pc_grid.append(pc_row)
        for i in range(0,8):
            enemy_row = []
            for j in range(0,8):
                square = self.create_rectangle(8*40+100+j*40, 10+i*40, 8*40+100+(j+1)*40, 10+(i+1)*40, fill='blue')
                enemy_row.append(square)
            self.__enemy_grid.append(enemy_row)
        
    def replace_pc(self, coord_i, coord_j, collor):
        self.delete(self.__pc_grid[coord_i][coord_j])
        self.__pc_grid[coord_i][coord_j] = self.create_rectangle(50+coord_j*40, 10+coord_i*40, 50+(coord_j+1)*40, 10+(coord_i+1)*40, fill=collor)
        pass
    
    def replace_enemy(self, coord_i, coord_j, collor):
        self.delete(self.__enemy_grid[coord_i][coord_j])
        self.__enemy_grid[coord_i][coord_j] = self.create_rectangle(8*40+100+coord_j*40, 10+coord_i*40, 8*40+100+(coord_j+1)*40, 10+(coord_i+1)*40, fill=collor)
        pass
    
    def place_at(self, ship_type, direction, x, y):
        length = 4-ship_type
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
            coord_i = x + i*dir_x
            coord_j = y + i*dir_y
            self.delete(self.__pc_grid[coord_i][coord_j])
            self.__pc_grid[coord_i][coord_j] = self.create_rectangle(50+coord_j*40, 10+coord_i*40, 50+(coord_j+1)*40, 10+(coord_i+1)*40, fill='green')
            
        pass
        
class AtackScreen(tk.Frame):
    
    def __init__(self, master, service, table_grid):
        tk.Frame.__init__(self, master, relief=tk.SUNKEN, bg='gray', colormap='new', width=200, height=8*40+20)
        self.__service = service
        self.__table_grid = table_grid
        
        coord_x_label = tk.Label(text='X coord:', bg='gray')
        coord_y_label = tk.Label(text='Y coord:', bg='gray')
        self.coord_x_entry = tk.Entry()
        self.coord_y_entry = tk.Entry()
        
        coord_x_label.place(x=5, y=20)
        coord_y_label.place(x=5, y=70)
        self.coord_x_entry.place(x=5, y=40)
        self.coord_y_entry.place(x=5, y=90)
        
        def send_hit():
            try:
                coord_i = int(str(self.coord_x_entry.get()))
                coord_j = int(str(self.coord_y_entry.get()))
            except:
                messagebox.showerror('Error', 'Non integer coordinate')
                return
            
            result = None
            try:
                result = self.__service.hit(coord_i, coord_j)
            except CustomError as ex:
                messagebox.showerror('Error', str(ex))
                return
            
            collor = 'red'
            if not result[0]:
                collor = 'black'
            
            self.__table_grid.replace_enemy(coord_i, coord_j, collor)
            
            coord_i = result[1]
            coord_j = result[2]
            
            collor = 'red'
            if not result[3]:
                collor = 'black'
            
            self.__table_grid.replace_pc(coord_i, coord_j, collor)
        
        send_button = tk.Button(self, relief=tk.SUNKEN, text ="Hit", command = send_hit)
        send_button.place(x=5, y=129)
        
        def debug():
            msg = self.__service.debug()
            messagebox.showwarning('Debug', msg)
        
        debug_button = tk.Button(self, relief=tk.SUNKEN, bg='red', text ="Debug", command = debug)
        debug_button.place(x=5, y=200)
        
    pass    
    
class ShipScreen(tk.Frame):
    
    def actualise_info(self):
        ships = ["Battleship", "Cruiser", "Destroyer"]
        
        self.direction_label.destroy()
        self.direction_label = tk.Label(self, bg='gray', text='Direction of the {}'.format(ships[self.curent_ship]))
        self.direction_label.place(x=5, y=20)
        self.row_entry.delete(0, len(self.row_entry.get()))
        self.column_entry.delete(0, len(self.column_entry.get()))
        self.direction_combo_box.current(0)
    
    def __init__(self, master, service, table_grid, atack_screen):
        tk.Frame.__init__(self, master, relief=tk.SUNKEN, bg='gray', width=200, height=8*40+20, colormap='new')
        self.curent_ship = 0
        self.__service = service
        self.__table_grid = table_grid
        self.__atack_screen = atack_screen
        
        self.direction_label = tk.Label(self, bg='gray', text='Direction of the {}'.format('not yet defined'))
        row_label = tk.Label(self, text='Row: ', bg='Gray')
        column_label = tk.Label(self, text='Column: ', bg='gray')
        self.row_entry = tk.Entry(self)
        self.column_entry = tk.Entry(self)
        self.direction_combo_box = ttk.Combobox(self, values=["South", "North", "East", "West"])
        
        self.direction_label.place(x=5, y=20)
        self.direction_combo_box.place(x=5, y=40)
        self.direction_combo_box.current(1)
        row_label.place(x=5, y=70)
        self.row_entry.place(x=5, y=90)
        column_label.place(x=5, y=120)
        self.column_entry.place(x=5, y=140)
        
        self.actualise_info()
        def submit_info():
            direction = self.direction_combo_box.current()
            coord_x = self.row_entry.get()
            coord_y = self.column_entry.get()
            self.actualise_info()
            try:
                coord_x = int(str(coord_x))
                coord_y = int(str(coord_y))
            except:
                messagebox.showerror('Error', 'Non integer coordinates')
                return
            
            try:
                self.__service.place_at(self.curent_ship, direction, coord_x, coord_y, is_enemy=False)
            except CustomError as ex:
                messagebox.showerror('Error', str(ex))
                return
            
            self.__table_grid.place_at(self.curent_ship, direction, coord_x, coord_y)
            
            self.curent_ship += 1
            if self.curent_ship == 3:
                self.__service.create_ai()
                self.__atack_screen.grid(row=0, column=0)
                self.destroy()
                return
            self.actualise_info()
            pass
        send_button = tk.Button(self, relief=tk.SUNKEN, text ="Place Ship", command = submit_info)
        send_button.place(x=5, y=200)
        
class GUI():
    
    def __init__(self, service):
        
        self.__service = service
        
        self.__root = tk.Tk()
        self.__root.title('Battleships')
        
        self.__tables = TableGrid(self.__root)
        self.__atack_screen = AtackScreen(self.__root, self.__service, self.__tables)
        self.__ships_screen = ShipScreen(self.__root, self.__service, self.__tables, self.__atack_screen)
        
        self.__ships_screen.grid(row=0, column=0)
        self.__tables.grid(row=0, column=1)
        self.__root.mainloop()
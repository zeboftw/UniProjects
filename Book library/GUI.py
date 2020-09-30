from tkinter import Tk, Frame, Button, Menu, Listbox, messagebox
from tkinter.constants import LEFT, TOP, BOTH, RIGHT, SINGLE, BUTT
from tkinter.ttk import Combobox, Entry
from Entities.class_CustomError import CustomError
from datetime import date

class GUI():
    
    def __init__(self, book_service, client_service, rental_service, undo_service):
        self.__book_service = book_service
        self.__client_service = client_service
        self.__rental_service = rental_service
        self.__undo_service = undo_service
        
        self.__root = Tk()
        self.__frame_action = Frame(self.__root, bg='blue')
        self.__frame_action.pack(side=LEFT)
        
        self.__add_button = Button(self.__frame_action, text='Add', width=20, height=3, command=self.request_data_add)
        self.__add_button.pack(padx=1, pady=1, side=TOP)
        
        self.__remove_button = Button(self.__frame_action, text='Remove', width=20, height=3, command=self.request_data_remove)
        self.__remove_button.pack(padx=1, pady=1, side=TOP)
        
        self.__update_button = Button(self.__frame_action, text='Update', width=20, height=3, command=self.request_data_update)
        self.__update_button.pack(padx=1, pady=1, side=TOP)
        
        self.__list_button = Button(self.__frame_action, text='List', width=20, height=3, command=self.request_list)
        self.__list_button.pack(padx=1, pady=1, side=TOP)
        
        self.__rent_button = Button(self.__frame_action, text='Rent', width=20, height=3, command=self.request_data_rent)
        self.__rent_button.pack(padx=1, pady=1, side=TOP)
        
        self.__return_button = Button(self.__frame_action, text='Return', width=20, height=3, command=self.request_data_return)
        self.__return_button.pack(padx=1, pady=1, side=TOP)
        
        self.__search_button = Button(self.__frame_action, text='Search', width=20, height=3, command=self.request_search)
        self.__search_button.pack(padx=1, pady=1, side=TOP)
        
        self.__top_button = Button(self.__frame_action, text='Top', width=20, height=3, command=self.request_top)
        self.__top_button.pack(padx=1, pady=1, side=TOP)
        
        self.__undo_button = Button(self.__frame_action, text='Undo', width=20, height=3, command=self.undo)
        self.__undo_button.pack(padx=1, pady=1, side=TOP)
        
        self.__redo_button = Button(self.__frame_action, text='Redo', width=20, height=3, command=self.redo)
        self.__redo_button.pack(padx=1, pady=1, side=TOP)
        
        self.__data_frame = Frame(self.__root)
        self.__data_frame.pack(side=LEFT)
        
        self.__running_process = False
        self.__root.geometry('200x400')
        self.__root.mainloop()
        
    def request_data_add(self):
        if self.__running_process is True:
            messagebox.showerror('Error', 'Already running a process!')
        else:
            self.__running_process = True
            persistent = Frame(self.__data_frame)
            persistent.pack(side=TOP)
            self.temp = Frame(self.__data_frame)
            self.temp.pack(side=TOP)
            
            combobox = Combobox(persistent, values=['Book', 'Client'])
            
            def update(event):
                self.temp.pack_forget()
                self.temp = Frame(self.__data_frame)
                
                if combobox.current() == 0:
                    book_id_entry = Entry(self.temp)
                    book_id_entry.pack(side=TOP)
                    book_title_entry = Entry(self.temp)
                    book_title_entry.pack(side=TOP)
                    book_author_entry = Entry(self.temp)
                    book_author_entry.pack(side=TOP)
                    
                    def submit_book():
                        book_id = int(str(book_id_entry.get()))
                        book_title = book_title_entry.get()
                        book_author = book_author_entry.get()
                        try:
                            self.__book_service.add_new_book(book_id, book_title, book_author)
                            messagebox.showinfo('Succes!', 'Succesfuly added the book!')
                            self.__running_process = False
                            self.__data_frame.pack_forget()
                            self.__data_frame = Frame(self.__root)
                            self.__data_frame.pack(side=LEFT)
                        except CustomError as ex:
                            messagebox.showerror('Error', str(ex))
                    
                    submit_button = Button(self.temp, width=10, height=2, text='Submit', command=submit_book)
                    submit_button.pack(side=TOP)
                else:
                    entry_client_id = Entry(self.temp)
                    entry_client_name = Entry(self.temp)
                    entry_client_id.pack(side=TOP)
                    entry_client_name.pack(side=TOP)
                    
                    def submit_client():
                        client_id = int(str(entry_client_id.get()))
                        client_name = entry_client_name.get()
                        try:
                            self.__client_service.add_new_client(client_id, client_name)
                            messagebox.showinfo('Succes!', 'Succesfuly added the client!')
                        except CustomError as ex:
                            messagebox.showerror('Error', str(ex))
                    submit_button = Button(self.temp, width=10, height=2, text='Submit', command=submit_client)
                    submit_button.pack(side=TOP)
                    
                self.temp.pack(side=TOP)
            
            combobox.bind("<<ComboboxSelected>>", update)
            
            combobox.grid(column=0, row=1)
            combobox.current(1)
    
    def request_data_remove(self):
        if self.__running_process is True:
            messagebox.showerror('Error', 'Aleady running a process!')
        else:
            combo_box = Combobox(self.__data_frame, values=['Book', 'Client'])
            combo_box.pack(side=TOP)
            combo_box.current(1)
            entry_id = Entry(self.__data_frame)
            entry_id.pack(side=TOP)
            
            def submit_remove():
                id = int(str(entry_id.get()))
                try:
                    if combo_box.current() == 0:
                        self.__rental_service.remove_book_and_rentals(id)
                    else:
                        self.__rental_service.remove_client_and_rentals(id)
                    messagebox.showinfo('Succes!', 'Removed element and associated rentals')
                    self.__data_frame.pack_forget()
                    self.__data_frame = Frame(self.__root)
                    self.__data_frame.pack(side=LEFT)
                    self.__running_process = False
                except CustomError as ex:
                    messagebox.showerror('Error!', str(ex))
                    
            button_submit = Button(self.__data_frame, width=10, height=2, text='Submit', command=submit_remove)
            button_submit.pack(side=TOP)
    
    def request_data_update(self):
        if self.__running_process is True:
            messagebox.showerror('Error', 'Already running a process!')
        else:
            self.__running_process = True
            persistent = Frame(self.__data_frame)
            persistent.pack(side=TOP)
            self.temp = Frame(self.__data_frame)
            self.temp.pack(side=TOP)
            
            combobox = Combobox(persistent, values=['Book', 'Client'])
            
            def update(event):
                self.temp.pack_forget()
                self.temp = Frame(self.__data_frame)
                
                if combobox.current() == 0:
                    book_id_entry = Entry(self.temp)
                    book_id_entry.pack(side=TOP)
                    book_title_entry = Entry(self.temp)
                    book_title_entry.pack(side=TOP)
                    book_author_entry = Entry(self.temp)
                    book_author_entry.pack(side=TOP)
                    
                    def submit_book():
                        book_id = int(str(book_id_entry.get()))
                        book_title = book_title_entry.get()
                        book_author = book_author_entry.get()
                        try:
                            self.__book_service.update_book(book_id, book_title, book_author)
                            messagebox.showinfo('Succes!', 'Succesfuly updated the book!')
                            self.__running_process = False
                            self.__data_frame.pack_forget()
                            self.__data_frame = Frame(self.__root)
                            self.__data_frame.pack(side=LEFT)
                        except CustomError as ex:
                            messagebox.showerror('Error', str(ex))
                    
                    submit_button = Button(self.temp, width=10, height=2, text='Submit', command=submit_book)
                    submit_button.pack(side=TOP)
                else:
                    entry_client_id = Entry(self.temp)
                    entry_client_name = Entry(self.temp)
                    entry_client_id.pack(side=TOP)
                    entry_client_name.pack(side=TOP)
                    
                    def submit_client():
                        client_id = int(str(entry_client_id.get()))
                        client_name = entry_client_name.get()
                        try:
                            self.__client_service.update_client(client_id, client_name)
                            messagebox.showinfo('Succes!', 'Succesfuly updated the client!')
                        except CustomError as ex:
                            messagebox.showerror('Error', str(ex))
                    submit_button = Button(self.temp, width=10, height=2, text='Submit', command=submit_client)
                    submit_button.pack(side=TOP)
                    
                self.temp.pack(side=TOP)
            
            combobox.bind("<<ComboboxSelected>>", update)
            
            combobox.grid(column=0, row=1)
            combobox.current(1)
    
    def request_list(self):
        if self.__running_process is True:
            messagebox.showerror('Error', 'Aleady running a process!')
        else:
            combo_box = Combobox(self.__data_frame, values=['Book','Client','Rental'])
            combo_box.pack(side=TOP)
            combo_box.current(0)
            
            def submit():
                elements = []
                if combo_box.current() == 0:
                    elements = self.__book_service.list_all()
                elif combo_box.current() == 1:
                    elements = self.__client_service.list_all()
                else:
                    elements = self.__rental_service.list_all()
                    
                message = ''
                for element in elements:
                    message += str(element) + '\n'
                    
                messagebox.showinfo('Elements', message)
                self.__data_frame.pack_forget()
                self.__data_frame = Frame(self.__root)
                self.__data_frame.pack(side=LEFT)
                self.__running_process = False
            
            button_submit = Button(self.__data_frame, width=10, height=2, text='Submit', command=submit)
            button_submit.pack(side=TOP)
            
    def request_data_rent(self):
        if self.__running_process is True:
            messagebox.showerror('Error', 'Aleady running a process!')
        else:
            entry_rental_id = Entry(self.__data_frame)
            entry_rental_id.pack(side=TOP)
            entry_book_id= Entry(self.__data_frame)
            entry_book_id.pack(side=TOP)
            entry_client_id = Entry(self.__data_frame)
            entry_client_id.pack(side=TOP)
            entry_date_year = Entry(self.__data_frame)
            entry_date_year.pack(side=TOP)
            entry_date_month = Entry(self.__data_frame)
            entry_date_month.pack(side=TOP)
            entry_date_day = Entry(self.__data_frame)
            entry_date_day.pack(side=TOP)
            
            def sumbit():
                rental_id = int(str(entry_rental_id.get()))
                book_id = int(str(entry_book_id.get()))
                client_id = int(str(entry_client_id.get()))
                date_year = int(str(entry_date_year.get()))
                date_month = int(str(entry_date_month.get()))
                date_day = int(str(entry_date_day.get()))
                
                try:
                    self.__rental_service.rent(rental_id, book_id, client_id, date_year, date_month, date_day)
                    messagebox.showinfo('Success!', 'Rented book!')
                    self.__data_frame.pack_forget()
                    self.__data_frame = Frame(self.__root)
                    self.__data_frame.pack(side=LEFT)
                    self.__running_process = False
                except CustomError as ex:
                    messagebox.showerror('Error!', str(ex))
                
                button_submit = Button(self.__data_frame, width=10, height=2, text='Submit', command=submit)
                button_submit.pack(side=TOP)
    
    def request_data_return(self):
        if self.__running_process is True:
            messagebox.showerror('Error', 'Aleady running a process!')
        else:
            entry_book_id = Entry(self.__data_frame)
            entry_book_id.pack(side=TOP)
            
            def submit():
                book_id = int(str(entry_book_id.get()))
                
                try:
                    self.__rental_service.return_book(book_id)
                    messagebox.showinfo('Success!', 'Returned book!')
                    self.__data_frame.pack_forget()
                    self.__data_frame = Frame(self.__root)
                    self.__data_frame.pack(side=LEFT)
                    self.__running_process = False
                except CustomError as ex:
                    messagebox.showerror('Error', str(ex))
                    
                button_submit = Button(self.__data_frame, width=10, height=2, text='Submit', command=submit)
                button_submit.pack(side=TOP)
    
    def request_search(self):
        if self.__running_process is True:
            messagebox.showerror('Error', 'Already running a process!')
        else:
            self.__running_process = True
            persistent = Frame(self.__data_frame)
            persistent.pack(side=TOP)
            self.temp = Frame(self.__data_frame)
            self.temp.pack(side=TOP)
            
            combobox = Combobox(persistent, values=['Book', 'Client'])
            
            def update(event):
                self.temp.pack_forget()
                self.temp = Frame(self.__data_frame)
                
                if combobox.current() == 0:
                    combo_box_fields = Combobox(self.temp, values=['id','title','author'])
                    combo_box_fields.pack(side=TOP)
                    
                    entry_search_term = Entry(self.temp)
                    entry_search_term.pack(side=TOP)
                    def get_books():
                        search_term = entry_search_term.get()
                        search_field = ''
                        if combo_box_fields.current() == 0:
                            search_term = int(str(search_term))
                            search_field = 'id'
                        elif combo_box_fields.current() == 1:
                            search_field = 'title'
                        else:
                            search_field = 'author'
                        try:
                            returned_elements = self.__book_service.search_book(search_field, search_term)
                            message = ''
                            for element in returned_elements:
                                message += str(element) + '\n'
                            messagebox.showinfo('Succes!', message)
                            self.__running_process = False
                            self.__data_frame.pack_forget()
                            self.__data_frame = Frame(self.__root)
                            self.__data_frame.pack(side=LEFT)
                        except CustomError as ex:
                            messagebox.showerror('Error', str(ex))
                    
                    submit_button = Button(self.temp, width=10, height=2, text='Submit', command=get_books)
                    submit_button.pack(side=TOP)
                else:
                    combo_box_fields = Combobox(self.temp, values=['id','name'])
                    combo_box_fields.pack(side=TOP)
                    
                    entry_search_term = Entry(self.temp)
                    entry_search_term.pack(side=TOP)
                    def get_clients():
                        search_term = entry_search_term.get()
                        search_field = ''
                        if combo_box_fields.current() == 0:
                            search_term = int(str(search_term))
                            search_field = 'id'
                        else:
                            search_field = 'name'
                        try:
                            returned_elements = self.__book_service.search_book(search_field, search_term)
                            message = ''
                            for element in returned_elements:
                                message += str(element) + '\n'
                            messagebox.showinfo('Succes!', message)
                            self.__running_process = False
                            self.__data_frame.pack_forget()
                            self.__data_frame = Frame(self.__root)
                            self.__data_frame.pack(side=LEFT)
                        except CustomError as ex:
                            messagebox.showerror('Error', str(ex))
                    
                    submit_button = Button(self.temp, width=10, height=2, text='Submit', command=get_clients)
                    submit_button.pack(side=TOP)
                    
                self.temp.pack(side=TOP)
            
            combobox.bind("<<ComboboxSelected>>", update)
            
            combobox.grid(column=0, row=1)
            combobox.current(1)
    
    
    def request_top(self):
        if self.__running_process is True:
            messagebox.showerror('Error', 'Aleady running a process!')
        else:
            combo_box = Combobox(self.__data_frame, values=['Most rented book', 'Most rented author', 'Most active client'])
            combo_box.pack(side=TOP)
            
            def submit():
                returned_elements = []
                type = ''
                if combo_box.current() == 0:
                    type = 'book'
                elif combo_box.current() == 1:
                    type = 'author'
                else:
                    type = 'client'
                try:
                    returned_elements = self.__rental_service.top(type)
                    message = ''
                    for element in returned_elements:
                        message += str(element) + '\n'
                    messagebox.showinfo('Success!', message)
                    self.__data_frame.pack_forget()
                    self.__data_frame = Frame(self.__root)
                    self.__data_frame.pack(side=LEFT)
                    self.__running_process = False
                except CustomError as ex:
                    messagebox.showerror('Error', str(ex))
            
            button_submit = Button(self.__data_frame, width=10, height=2, text='Submit', command=submit)
            button_submit.pack(side=TOP)
            
    def undo(self):
        try:
            self.__undo_service.undo()
            messagebox.showinfo('Success!', 'Undid!')
        except CustomError as ex:
            messagebox.showerror('Error', str(ex))
    
    def redo(self):
        try:
            self.__undo_service.redo()
            messagebox.showinfo('Success!', 'Redid!')
        except CustomError as ex:
            messagebox.showerror('Error', str(ex))
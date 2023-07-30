import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('App')
        self.geometry('1000x400')
        self.minsize(800, 400)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure((0), weight=0)
        self.columnconfigure((1), weight=1)

        self.form = Form(self)
        self.search = Toolbar(self)
        self.table = Table(self)
        self.navigation = Navigation(self)
        
        self.mainloop()

class Table(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.create_widgets()
        self.grid(row=1, column=1, sticky='nsew', padx=25, pady=0)

    def create_widgets(self):
        tree_scroll = ttk.Scrollbar(self)

        self.treeview = ttk.Treeview(self, columns=('Name', 'Receipt', 'Item', 'Quantity'), show='headings')
        self.treeview.heading('Name', text='Name', command=lambda: self.sort_column(self.treeview, 'Name'))
        self.treeview.column('Name', anchor='center', minwidth=50)
        self.treeview.heading('Receipt', text='Receipt', command=lambda: self.sort_column(self.treeview, 'Receipt'))
        self.treeview.column('Receipt', anchor='center', minwidth=50, width=150)
        self.treeview.heading('Item', text='Item', command=lambda: self.sort_column(self.treeview, 'Item'))
        self.treeview.column('Item', anchor='center', minwidth=50)
        self.treeview.heading('Quantity', text='Quantity', command=lambda: self.sort_column(self.treeview, 'Quantity'))
        self.treeview.column('Quantity', anchor='center', minwidth=60, width=60)

        self.treeview.grid(column=0, row=0, sticky='nsew')
        tree_scroll.grid(column=1, row=0, sticky='ns')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

class Form(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.create_widgets()
        self.grid(column=0, row=1, sticky='new', padx=5, pady=50)

    def create_widgets(self):
        self.name_label = ttk.Label(self, text='Full Name')
        self.name_entry = ttk.Entry(self)

        self.receipt_label = ttk.Label(self, text='Receipt Number')
        self.receipt_entry = ttk.Entry(self)

        self.item_label = ttk.Label(self, text='Item')
        self.item_entry = ttk.Entry(self)

        self.quantity_label = ttk.Label(self, text='Quantity')
        self.quantity_entry = ttk.Entry(self)

        add_button = ttk.Button(self, text='Add', command=self.add_data)
        update_button = ttk.Button(self, text='Update', command=self.update_item)

        self.name_label.grid(row=0, column=0, pady=5)
        self.name_entry.grid(row=0, column=1, pady=5)

        self.receipt_label.grid(row=1, column=0, pady=5)
        self.receipt_entry.grid(row=1, column=1, pady=5)

        self.item_label.grid(row=2, column=0, pady=5)
        self.item_entry.grid(row=2, column=1, pady=5)

        self.quantity_label.grid(row=3, column=0, pady=5)
        self.quantity_entry.grid(row=3, column=1, pady=5)

        add_button.grid(row=4, column=0, sticky='', padx=10, pady=5, ipadx=25, ipady=2)
        update_button.grid(row=4, column=1, sticky='', padx=10, pady=5, ipadx=25, ipady=2)

        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

    def add_data(self):
        pass

    def update_item(self):
        pass

class Navigation(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.grid(row=2, column=1, padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):
        self.display_name_entry = ttk.Entry(self, state='readonly')
        self.receipt_name_entry = ttk.Entry(self, state='readonly')
        self.item_name_entry = ttk.Entry(self, state='readonly')
        self.quantity_name_entry = ttk.Entry(self, state='readonly')

        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.rowconfigure(0, weight=1)
        
        self.display_name_entry.grid(column=1, row=0, padx=2, pady=5)
        self.receipt_name_entry.grid(column=2, row=0, padx=2, pady=5)
        self.item_name_entry.grid(column=3, row=0, padx=2, pady=5)
        self.quantity_name_entry.grid(column=4, row=0, padx=2, pady=5)

        self.left_button = ttk.Button(self, text='<', command=self.navigate_left)
        self.right_button = ttk.Button(self, text='>', command=self.navigate_right)

        self.left_button.grid(column=0, row=0, padx=2, pady=5)
        self.right_button.grid(column=5, row=0, padx=2, pady=5)

    def navigate_left(self):
        pass

    def navigate_right(self):
        pass

class Toolbar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.grid(row=0, column=1, padx=(24, 40), pady=10, sticky='ew')

        self.create_widgets()

    def create_widgets(self):
        self.search_bar = ttk.Entry(self, width=40)
        self.search_bar_button = ttk.Button(self, text='Search')
        self.delete = ttk.Button(self, text='Delete')

        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.delete.grid(column=0, row=0, sticky='w')
        self.search_bar.grid(column=1, row=0, sticky='e')
        self.search_bar_button.grid(column=1, row=0, sticky='e')

app = App()
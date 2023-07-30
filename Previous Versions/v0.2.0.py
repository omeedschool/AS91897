import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

data_list = []
selected_data = []
selected_id = []
multi_select = False

string_data_list = ('XXXXXX', 'YYYYYY', 'ZZZZZZ')
int_data_list = ('111111', '111111', '222222', '333333')

for i in range(1, 10):
    first = random.choice(string_data_list)
    receipt = random.choice(int_data_list)
    item = random.choice(string_data_list)
    quantity = random.choice(int_data_list)
    data = (first, receipt, item, quantity)
    data_list.append(data)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('App')
        self.minsize(800, 400)

        window_width = 1000
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 100

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

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

        self.current_sort_column = None
        self.current_sort_reverse = False

        self.grid(row=1, column=1, sticky='nsew', padx=25, pady=0)

        self.create_widgets()

        self.update_treeview(data_list)

    def create_widgets(self):
        tree_scroll = ttk.Scrollbar(self)
        self.treeview = ttk.Treeview(self, columns=('Name', 'Receipt', 'Item', 'Quantity'), show='headings', yscrollcommand=tree_scroll.set)

        self.treeview.heading('Name', text='Name', command=lambda: self.sort_column(self.treeview, 'Name'))
        self.treeview.column('Name', anchor='center', minwidth=50)
        self.treeview.heading('Receipt', text='Receipt', command=lambda: self.sort_column(self.treeview, 'Receipt'))
        self.treeview.column('Receipt', anchor='center', minwidth=50, width=150)
        self.treeview.heading('Item', text='Item', command=lambda: self.sort_column(self.treeview, 'Item'))
        self.treeview.column('Item', anchor='center', minwidth=50)
        self.treeview.heading('Quantity', text='Quantity', command=lambda: self.sort_column(self.treeview, 'Quantity'))
        self.treeview.column('Quantity', anchor='center', minwidth=60, width=60)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.treeview.grid(column=0, row=0, sticky='nsew')
        tree_scroll.grid(column=1, row=0, sticky='ns')

        tree_scroll.config(command=self.treeview.yview)

        self.treeview.bind('<<TreeviewSelect>>', self.item_select)
        self.treeview.bind('<Delete>', self.delete_items)
        self.treeview.bind('<Button-3>', self.right_click)

    def update_treeview(self, treeview_data):
        self.treeview.delete(*self.treeview.get_children())

        for data in treeview_data:
            self.treeview.insert('', 'end', values=data)

        global selected_data
        global selected_id
        selected_data = []
        selected_id = []

    def search(self, query):
        searched_data = []

        for item in data_list:
            found = False
            for value in item:
                if query.lower() in str(value).lower():
                    found = True
                    break
            if found:
                searched_data.append(item)

        self.update_treeview(searched_data)

        if query == '':
            self.update_treeview(data_list)

    def add_item(self, name, receipt, item, quantity):
        data = (name, receipt, item, quantity)
        data_list.insert(0, data)

    def sort_column(self, treeview, column):
        if self.current_sort_column == column:
            self.current_sort_reverse = not self.current_sort_reverse
        else:
            self.current_sort_column = column
            self.current_sort_reverse = False

        data = [(int(treeview.set(child, column)) if column in ['Receipt', 'Quantity'] else treeview.set(child, column), child) for child in treeview.get_children('')]

        data.sort(reverse=self.current_sort_reverse)

        for index, (value, child) in enumerate(data):
            treeview.move(child, '', index)

        for col in treeview['columns']:
            if col != column:
                treeview.heading(col, text=col)

        sort_arrow = '↑' if not self.current_sort_reverse else '↓'
        treeview.heading(column, text=f'{column} {sort_arrow}')

    def item_select(self, event):
        global selected_data
        global selected_id
        global multi_select
        selected_data = []
        for item in event.widget.selection():
            selected_data = event.widget.item(item)['values']
            selected_id = event.widget.selection()
            self.master.form.selected_item = selected_data

            self.master.navigation.update_display(selected_data)
            self.master.form.update_entry_box(selected_data)
        multi_select = False

        if len(event.widget.selection()) > 1:
            selected_data = []
            for item in event.widget.selection():
                selected_data.append(event.widget.item(item)['values'])
            multi_select = True

        print(selected_data)

    def delete_items(self, event=None):
        global selected_data
        global multi_select

        item_found = False

        if selected_data:
            confirmed = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected item(s)?")
            if confirmed:
                if multi_select == True:
                    for x in selected_data:
                        for items in data_list:
                            h = [(x[0], str(x[1]), x[2], str(x[3]))]
                            if h[0] == items:
                                data_list.remove(items)
                else:

                    i = [(selected_data[0], str(selected_data[1]), selected_data[2], str(selected_data[3]))]
                    if item_found == False:
                        for items in data_list:
                            if i[0] == items:
                                data_list.remove(items)
                                item_found = True

                self.update_treeview(data_list)

                selected_data = []
                selected_id = []
                self.master.navigation.update_display(selected_data)
                self.master.form.update_entry_box()
        else:
            messagebox.showwarning("No Item Selected", "Please select item(s) to delete.")

    def right_click(self, event):
        selected_item = event.widget.identify('item', event.x, event.y)
        if selected_item:
            data = event.widget.item(selected_item)['values']
            show_context_menu(event.widget, event.x_root, event.y_root, data)


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
        name = self.name_entry.get()
        receipt = self.receipt_entry.get()
        item = self.item_entry.get()
        quantity = self.quantity_entry.get()

        if name and receipt and item and quantity:
            data_list.append((name, receipt, item, quantity))
            self.master.table.update_treeview(data_list)
        else:
            messagebox.showwarning("Incomplete Data", "Please fill in all the fields.")

    def update_entry_box(self, selected_data=None):
        self.name_entry.delete(0, 'end')
        self.receipt_entry.delete(0, 'end')
        self.item_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')

        if selected_data:
            self.name_entry.insert(0, selected_data[0])
            self.receipt_entry.insert(0, selected_data[1])
            self.item_entry.insert(0, selected_data[2])
            self.quantity_entry.insert(0, selected_data[3])

    def update_item(self):
        global selected_data
        global multi_select

        name = self.name_entry.get()
        receipt = self.receipt_entry.get()
        item = self.item_entry.get()
        quantity = self.quantity_entry.get()

        if selected_data:
            if multi_select == True:
                for value in selected_data:
                    for items in data_list:
                        temp_str = [(value[0], str(value[1]), value[2], str(value[3]))]
                        if temp_str[0] == items:
                            data_list.remove(items)
                            self.master.table.add_item(name, receipt, item, quantity)
            else:
                temp_str = [(selected_data[0], str(selected_data[1]), selected_data[2], str(selected_data[3]))]
                for items in data_list:
                    if temp_str[0] == items:
                        data_list.remove(items)
                        self.master.table.add_item(name, receipt, item, quantity)
                        break

            self.master.table.update_treeview(data_list)

            self.master.navigation.update_display(selected_data)
            self.master.form.update_entry_box()

    def clear_entry_fields(self):
        self.name_entry.delete(0, 'end')
        self.receipt_entry.delete(0, 'end')
        self.item_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.selected_data = None


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

    def update_display(self, data):
        self.display_name_entry.config(state='normal')
        self.receipt_name_entry.config(state='normal')
        self.item_name_entry.config(state='normal')
        self.quantity_name_entry.config(state='normal')

        self.display_name_entry.delete(0, 'end')
        self.receipt_name_entry.delete(0, 'end')
        self.item_name_entry.delete(0, 'end')
        self.quantity_name_entry.delete(0, 'end')

        if data:
            self.display_name_entry.insert(0, data[0])
            self.receipt_name_entry.insert(0, data[1])
            self.item_name_entry.insert(0, data[2])
            self.quantity_name_entry.insert(0, data[3])

        self.display_name_entry.config(state='readonly')
        self.receipt_name_entry.config(state='readonly')
        self.item_name_entry.config(state='readonly')
        self.quantity_name_entry.config(state='readonly')

        self.data_list = data
        self.current_index = 0

    def navigate_left(self):
        tree = self.master.table.treeview
        selected_item = tree.selection()
        if selected_item:
            current_index = tree.index(selected_item[0])
            total_items = len(tree.get_children())
            new_index = (current_index - 1) % total_items
            new_item = tree.get_children()[new_index]
            tree.selection_set(new_item)
            self.update_display(tree.item(new_item)['values'])

    def navigate_right(self):
        tree = self.master.table.treeview
        selected_item = tree.selection()
        if selected_item:
            current_index = tree.index(selected_item[0])
            total_items = len(tree.get_children())
            new_index = (current_index + 1) % total_items
            new_item = tree.get_children()[new_index]
            tree.selection_set(new_item)
            self.update_display(tree.item(new_item)['values'])


class Toolbar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.grid(row=0, column=1, padx=(24, 41), pady=5, sticky='ew')

        self.create_widgets()

    def create_widgets(self):
        self.search_bar = ttk.Entry(self, width=40)
        self.search_bar_button = ttk.Button(self, text='Search', command=self.search_items)
        self.delete_button = ttk.Button(self, text='Delete', command=self.delete_items)
        self.clear_button = ttk.Button(self, text='Clear Search', command=self.clear_search)

        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1), weight=0)
        self.columnconfigure((2), weight=1)

        self.delete_button.grid(column=0, row=0, sticky='w')
        self.clear_button.grid(column=1, row=0, sticky='w')
        self.search_bar.grid(column=2, row=0, sticky='e')
        self.search_bar_button.grid(column=2, row=0, sticky='e')


    def delete_items(self):
        self.master.table.delete_items()

    def clear_search(self):
        self.master.table.search('')
        self.search_bar.delete(0, 'end')

    def search_items(self):
        query = self.search_bar.get()
        self.master.table.search(query)

def show_context_menu(widget, x, y, data):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label='Copy', command=lambda: copy_data(data))

    menu.post(x, y)

def copy_data(data):
    print('Data copied:', data)

    root = tk.Tk()
    root.withdraw()

    root.clipboard_clear()
    root.clipboard_append(data)

app = App()
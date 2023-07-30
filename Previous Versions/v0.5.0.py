import tkinter as tk
from tkinter import ttk, messagebox
import random

data_list = []


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("App")
        self.minsize(800, 400)

        window_width = 1000
        window_height = 500

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 100

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.form = Form(self)
        self.toolbar = Toolbar(self)
        self.data_table = DataTable(self)
        self.navigation = Navigation(self)

        self.mainloop()


class DataTable(ttk.Frame):

    selected_data = []
    selected_ids = []

    def __init__(self, parent):
        super().__init__(master=parent)

        self.current_sort_column = None
        self.current_sort_reverse = False

        self.grid(row=1, column=1, sticky="nsew", padx=25, pady=0)

        self.create_widgets()

        self.update_treeview(data_list)

    def create_widgets(self):

        tree_scrollbar = ttk.Scrollbar(self)

        self.treeview = ttk.Treeview(self, columns=(
            "Name", "Receipt", "Item", "Quantity"), show="headings", yscrollcommand=tree_scrollbar.set)

        self.treeview.heading(
            "Name", text="Name", command=lambda: self.sort_column(self.treeview, "Name"))
        self.treeview.column("Name", anchor="center", minwidth=50)

        self.treeview.heading("Receipt", text="Receipt", command=lambda: self.sort_column(
            self.treeview, "Receipt"))
        self.treeview.column("Receipt", anchor="center",
                             minwidth=50, width=150)

        self.treeview.heading(
            "Item", text="Item", command=lambda: self.sort_column(self.treeview, "Item"))
        self.treeview.column("Item", anchor="center", minwidth=50)

        self.treeview.heading("Quantity", text="Quantity", command=lambda: self.sort_column(
            self.treeview, "Quantity"))
        self.treeview.column("Quantity", anchor="center",
                             minwidth=60, width=60)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.treeview.grid(column=0, row=0, sticky="nsew")
        tree_scrollbar.grid(column=1, row=0, sticky="ns")

        tree_scrollbar.config(command=self.treeview.yview)

        self.treeview.bind("<<TreeviewSelect>>", self.item_select)
        self.treeview.bind("<Delete>", self.delete_items)
        self.treeview.bind("<Button-3>", self.right_click)

    def item_select(self, event):

        self.selected_ids = event.widget.selection()

        self.selected_data = [tuple(value for value in event.widget.item(item)[
                                    "values"]) for item in self.selected_ids]

        self.master.form.update_entry_box(self.selected_data)
        self.master.navigation.update_display(self.selected_data)

    def update_item(self):

        name = self.master.form.name_entry.get()
        receipt = self.master.form.receipt_entry.get()
        item = self.master.form.item_entry.get()
        quantity = self.master.form.quantity_entry.get()

        if not (name and receipt and item and quantity):
            messagebox.showwarning(
                "Incomplete Data", "Please fill in all the fields.")
            return

        try:
            int(quantity)
            if int(quantity) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Quantity", "Quantity should be a positive integer.")
            return

        try:
            int(receipt)
            if int(receipt) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Receipt", "Receipt should be a positive integer")
            return

        if len(self.selected_data) > 1 and self.selected_data:
            for data in self.selected_data:
                index = data_list.index(data)
                data_list[index] = (name, int(receipt), item, int(quantity))
        else:
            if self.selected_data:
                index = data_list.index(self.selected_data[0])
                data_list[index] = (name, int(receipt), item, int(quantity))

        self.update_treeview(data_list)

    def update_treeview(self, treeview_data):

        self.treeview.delete(*self.treeview.get_children())

        for data in treeview_data:
            self.treeview.insert("", "end", values=data)

        self.selected_data = []
        self.selected_ids = []

    def search(self, query):

        searched_items = []

        for item in data_list:
            found = False
            for value in item:
                if query.lower() in str(value).lower():
                    found = True
                    break
            if found:
                searched_items.append(item)

        self.update_treeview(searched_items)

        if not query:
            self.update_treeview(data_list)

    def add_item(self, name, receipt, item, quantity):

        data = (name, receipt, item, quantity)
        data_list.insert(0, data)

    def delete_items(self, event=None):

        self.selected_ids = self.treeview.selection()

        if self.selected_ids:
            response = messagebox.askyesno(
                "Delete Items", "Are you sure you want to delete the selected items?")
            if response:
                selected_indexes = [self.treeview.index(
                    item) for item in self.selected_ids]
                selected_indexes.sort(reverse=True)

                for index in selected_indexes:
                    del data_list[index]

                self.update_treeview(data_list)
        else:
            messagebox.showwarning(
                "No Selection", "Please select items to delete.")

    def return_items(self):
        selected = self.selected_data

        if len(selected) == 1:
            def return_action(option, amount=None):
                if option == "Return":
                    self.return_single_item(selected, amount)
                elif option == "Return All":
                    self.return_all_items(selected)
                return_toplevel.destroy()

            return_toplevel = tk.Toplevel(self.master)
            return_toplevel.focus_force()
            return_toplevel.title("Returned Item")
            return_toplevel.geometry("300x120")
            return_toplevel.maxsize(300, 120)
            return_toplevel.minsize(300, 120)

            return_label = ttk.Label(return_toplevel, text="Return Amount")
            amount_entry = ttk.Entry(return_toplevel)
            return_button = ttk.Button(return_toplevel, text="Return", command=lambda: return_action(
                "Return", amount_entry.get()))
            return_all_button = ttk.Button(
                return_toplevel, text="Return All", command=lambda: return_action("Return All"))

            return_label.pack()
            amount_entry.pack()
            return_button.pack(pady=(10, 0))
            return_all_button.pack()

        else:
            messagebox.showwarning("Too many selected",
                                   "Please return only one item type")

    def return_single_item(self, selected, amount):
        name = selected[0][0]
        receipt = selected[0][1]
        item = selected[0][2]
        quantity = selected[0][3]

        try:
            int(amount)
            if int(amount) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Quantity", "Quantity should be a positive integer.")
            return

        if selected:
            new_amount = int(quantity) - int(amount)
            if new_amount == 0:
                self.return_all_items(selected)
            elif new_amount < 0:
                messagebox.showerror(
                    "Error", "Amount of item returned exceeded item hired")
            else:
                print(self.selected_data)
                index = data_list.index(self.selected_data[0])
                data_list[index] = (name, receipt, item, new_amount)
                self.update_treeview(data_list)

    def return_all_items(self, selected):
        self.delete_items()

    def sort_column(self, treeview, column):

        if self.current_sort_column == column:
            self.current_sort_reverse = not self.current_sort_reverse
        else:
            self.current_sort_column = column
            self.current_sort_reverse = False

        column_index = {
            "Name": 0,
            "Receipt": 1,
            "Item": 2,
            "Quantity": 3
        }[column]

        data_list.sort(
            key=lambda item: item[column_index], reverse=self.current_sort_reverse)
        self.update_treeview(data_list)

        for col in treeview["columns"]:
            if col != column:
                treeview.heading(col, text=col)

        sort_arrow = "↑" if not self.current_sort_reverse else "↓"
        treeview.heading(column, text=f"{column} {sort_arrow}")

    def right_click(self, event):

        selected_item = event.widget.identify("item", event.x, event.y)
        if selected_item:
            data = event.widget.item(selected_item)["values"]
            show_context_menu(event.widget, event.x_root, event.y_root, data)


class Form(ttk.Frame):

    def __init__(self, parent):
        super().__init__(master=parent)

        self.create_widgets()
        self.grid(column=0, row=1, sticky="new", padx=5, pady=50)

    def create_widgets(self):

        self.name_label = ttk.Label(self, text="Full Name")
        self.name_entry = ttk.Entry(self)

        self.receipt_label = ttk.Label(self, text="Receipt Number")
        self.receipt_entry = ttk.Entry(self)

        self.item_label = ttk.Label(self, text="Item")
        self.item_entry = ttk.Entry(self)

        self.quantity_label = ttk.Label(self, text="Quantity")
        self.quantity_entry = ttk.Entry(self)

        self.add_button = ttk.Button(self, text="Add", command=self.add_data)
        self.return_button = ttk.Button(
            self, text="Return", command=self.return_item)
        self.update_button = ttk.Button(
            self, text="Update", command=self.update_item)
        self.clear_entries_button = ttk.Button(
            self, text="Clear Entries", command=self.clear_entry_fields)
        self.update_all_button = ttk.Button(
            self, text="Update All", command=self.update_multiple_items)

        self.name_label.grid(row=0, column=0, pady=5)
        self.name_entry.grid(row=0, column=1, pady=5)

        self.receipt_label.grid(row=1, column=0, pady=5)
        self.receipt_entry.grid(row=1, column=1, pady=5)

        self.item_label.grid(row=2, column=0, pady=5)
        self.item_entry.grid(row=2, column=1, pady=5)

        self.quantity_label.grid(row=3, column=0, pady=5)
        self.quantity_entry.grid(row=3, column=1, pady=5)

        self.add_button.grid(row=4, column=0, sticky="",
                             padx=10, pady=5, ipadx=25, ipady=2)
        self.update_button.grid(
            row=4, column=1, sticky="", padx=10, pady=5, ipadx=25, ipady=2)
        self.return_button.grid(
            row=5, column=0, sticky="", padx=10, pady=5, ipadx=25, ipady=2, columnspan=1)
        self.update_all_button.grid(
            row=5, column=1, sticky="", padx=10, pady=5, ipadx=25, ipady=2, columnspan=1)
        self.clear_entries_button.grid(
            row=6, column=0, sticky="", padx=10, pady=5, ipadx=25, ipady=2, columnspan=2)

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

    def update_multiple_items(self):

        response = messagebox.askyesno(
            "Update Items", "Are you sure you want to update the selected items?")
        if response:
            self.master.data_table.update_item()
            self.master.toolbar.clear_search()

    def add_data(self):

        name = self.name_entry.get()
        receipt = self.receipt_entry.get()
        item = self.item_entry.get()
        quantity = self.quantity_entry.get()

        if not (name and item and quantity):
            messagebox.showwarning(
                "Incomplete Data", "Please fill in all the fields.")
            return

        if not receipt:
            receipt = random.randint(10000, 99999)

        try:
            int(receipt)
            if int(receipt) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Receipt", "Receipt should be a positive integer.")
            return

        try:
            int(quantity)
            if int(quantity) <= 0 or int(quantity) > 500:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Quantity", "Quantity should be a positive integer between 1-500.")
            return

        if name.isdigit():
            messagebox.showwarning(
                "Invalid Name", "Name should not contain numbers.")
            return

        if item.isdigit():
            messagebox.showwarning(
                "Invalid Item", "Item name should not contain numbers.")
            return

        for item_data in data_list:
            if receipt == item_data[1]:
                prompt = messagebox.askyesnocancel(
                    "Duplicate Receipt Found", "Another item with the same receipt number was found, are you sure you want to add this item?")
                if prompt is None:
                    return
                elif prompt:
                    break
                else:
                    self.receipt_entry.delete(0, "end")
                    return

        data_list.append((name, int(receipt), item, int(quantity)))
        self.master.data_table.update_treeview(data_list)

    def return_item(self):
        self.master.data_table.return_items()

    def update_entry_box(self, selected_data=None):

        self.name_entry.delete(0, "end")
        self.receipt_entry.delete(0, "end")
        self.item_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")

        if selected_data:
            self.name_entry.insert(0, selected_data[0][0])
            self.receipt_entry.insert(0, selected_data[0][1])
            self.item_entry.insert(0, selected_data[0][2])
            self.quantity_entry.insert(0, selected_data[0][3])

    def update_item(self):

        if len(self.master.data_table.selected_data) > 1:
            messagebox.showwarning("Incorrect function",
                                   "Use 'Update All' to update multiple items")
        else:
            self.master.data_table.update_item()
            self.master.toolbar.clear_search()

    def clear_entry_fields(self):

        self.name_entry.delete(0, "end")
        self.receipt_entry.delete(0, "end")
        self.item_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.master.data_table.selected_data = None


class Navigation(ttk.Frame):

    def __init__(self, parent):
        super().__init__(master=parent)

        self.grid(row=2, column=1, padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):

        self.display_name_entry = ttk.Entry(self, state="readonly")
        self.receipt_name_entry = ttk.Entry(self, state="readonly")
        self.item_name_entry = ttk.Entry(self, state="readonly")
        self.quantity_name_entry = ttk.Entry(self, state="readonly")

        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.rowconfigure(0, weight=1)

        self.display_name_entry.grid(column=1, row=0, padx=2, pady=5)
        self.receipt_name_entry.grid(column=2, row=0, padx=2, pady=5)
        self.item_name_entry.grid(column=3, row=0, padx=2, pady=5)
        self.quantity_name_entry.grid(column=4, row=0, padx=2, pady=5)

        self.left_button = ttk.Button(
            self, text="<", command=self.navigate_left)
        self.right_button = ttk.Button(
            self, text=">", command=self.navigate_right)

        self.left_button.grid(column=0, row=0, padx=2, pady=5)
        self.right_button.grid(column=5, row=0, padx=2, pady=5)

    def update_display(self, data):

        self.display_name_entry.config(state="normal")
        self.receipt_name_entry.config(state="normal")
        self.item_name_entry.config(state="normal")
        self.quantity_name_entry.config(state="normal")

        self.display_name_entry.delete(0, "end")
        self.receipt_name_entry.delete(0, "end")
        self.item_name_entry.delete(0, "end")
        self.quantity_name_entry.delete(0, "end")

        if data:
            self.display_name_entry.insert(0, data[0][0])
            self.receipt_name_entry.insert(0, data[0][1])
            self.item_name_entry.insert(0, data[0][2])
            self.quantity_name_entry.insert(0, data[0][3])

        self.display_name_entry.config(state="readonly")
        self.receipt_name_entry.config(state="readonly")
        self.item_name_entry.config(state="readonly")
        self.quantity_name_entry.config(state="readonly")

    def navigate_left(self):

        tree = self.master.data_table.treeview
        selected_item = tree.selection()
        if selected_item:
            current_index = tree.index(selected_item[0])
            total_items = len(tree.get_children())
            new_index = (current_index - 1) % total_items
            new_item = tree.get_children()[new_index]
            tree.selection_set(new_item)
            self.update_display(tree.item(new_item)["values"])

    def navigate_right(self):

        tree = self.master.data_table.treeview
        selected_item = tree.selection()
        if selected_item:
            current_index = tree.index(selected_item[0])
            total_items = len(tree.get_children())
            new_index = (current_index + 1) % total_items
            new_item = tree.get_children()[new_index]
            tree.selection_set(new_item)
            self.update_display(tree.item(new_item)["values"])


class Toolbar(ttk.Frame):

    def __init__(self, parent):
        super().__init__(master=parent)

        self.grid(row=0, column=1, padx=(24, 41), pady=5, sticky="ew")

        self.create_widgets()

    def create_widgets(self):

        self.search_bar = ttk.Entry(self, width=40)
        self.search_bar_button = ttk.Button(
            self, text="Search", command=self.search_items)
        self.delete_button = ttk.Button(
            self, text="Delete", command=self.delete_items)
        self.clear_button = ttk.Button(
            self, text="Clear Search", command=self.clear_search)

        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1), weight=0)
        self.columnconfigure(2, weight=1)

        self.delete_button.grid(column=0, row=0, sticky="w")
        self.clear_button.grid(column=1, row=0, sticky="w")
        self.search_bar.grid(column=2, row=0, sticky="e")
        self.search_bar_button.grid(column=2, row=0, sticky="e")

    def delete_items(self):

        self.master.data_table.delete_items()

    def clear_search(self):

        self.master.data_table.search("")
        self.search_bar.delete(0, "end")

    def search_items(self):

        query = self.search_bar.get()
        self.master.data_table.search(query)


def show_context_menu(widget, x, y, data):

    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Copy", command=lambda: copy_data(data))
    menu.add_command(
        label="Return", command=lambda: widget.master.return_items())

    menu.post(x, y)


def copy_data(data):

    print("Data copied:", data)

    root = tk.Tk()
    root.withdraw()

    root.clipboard_clear()
    root.clipboard_append(data)


app = App()
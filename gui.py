import customtkinter as ctk
from customtkinter import CTkButton, CTkToplevel

from databasemanager import DatabaseManager
from tkinter import ttk

class BudgetPlannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Planer")
        self.geometry("1000x600")
        
        self.db = DatabaseManager()
        self.db.initialize_db()

        self.create_widgets()

    def create_widgets(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        
        self.tab_transactions = self.tabview.add("Transactions")
        self.tab_categories = self.tabview.add("Categories")

        frame_tree = ctk.CTkFrame(self.tab_categories)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame_tree, columns=("ID", "Parent-ID"), show="tree headings")
        self.tree.heading("#0", text="Category")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Parent-ID", text="Parent")
        self.tree.column("#0", width=200)
        self.tree.column("ID", width=0, stretch = False)
        self.tree.column("Parent-ID", width=80)
        self.tree.pack(fill="both", expand=True)
        
        frame_buttons = ctk.CTkFrame(self.tab_categories)
        frame_buttons.pack(fill="x", padx = 10, pady = 10)
        
        button_add = CTkButton(frame_buttons, text = "Add")
        button_add.pack(side="left", padx = 5)
        button_add.configure(command = self.open_add_category_dialog)
        
        button_edit = CTkButton(frame_buttons, text = "Edit")
        button_edit.pack(side="left", padx = 5)
        button_edit.configure(command = self.open_edit_category_dialog)
        
        button_del = CTkButton(frame_buttons, text = "Delete")
        button_del.pack(side="left", padx = 5)
        
        self.load_categories()
        
    def load_categories(self):
        self.tree.delete(*self.tree.get_children())
        self.category_map = {}
        rows = self.db.get_all_categories()
        name_by_id = {category_id: name for category_id, name, parent_id in rows}
        for row in rows:
            category_id, name, parent_id = row
            if parent_id is None:
                tree_id = self.tree.insert("", "end", text=name, values=(category_id, ""))
                self.category_map[category_id] = tree_id
                
        for row in rows:
            category_id, name, parent_id = row
            if parent_id is not None:
                parent_tree_id = self.category_map[parent_id]
                parent_name = name_by_id[parent_id]
                tree_id = self.tree.insert(parent_tree_id, "end", text=name, values=(category_id, parent_name))
                self.category_map[category_id] = tree_id            
     
    def open_add_category_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.focus_force()
        dialog.title("Add Category")
        dialog.geometry("500x300")
        
        ctk.CTkLabel(dialog, text = "Name: ").pack(pady = 5)
        name_entry = ctk.CTkEntry(dialog)
        name_entry.pack(pady = 5)
        
        ctk.CTkLabel(dialog, text = "Parent: ").pack(pady = 5)
        categories = self.db.get_categories()
        dropdown_names = ["None"]
        dropdown_ids = [None]
        subcategories_names = ["None"]
        subcategories_ids = [None]
        
        for category_id, name, parent_id in categories:
            dropdown_names.append(name)
            dropdown_ids.append(category_id)
            
        parent_option = ctk.CTkOptionMenu(dialog, values = dropdown_names)
        parent_option.pack(pady = 5)

        ctk.CTkLabel(dialog, text = "Subcategory: ").pack(pady = 10)
        
        child_option = ctk.CTkOptionMenu(dialog, values = subcategories_names, state = "disabled")
        child_option.pack(pady = 5)
        
        def save():
            selected_name = name_entry.get().strip()
            if not selected_name:
                return
            selected_parent_name = parent_option.get()
            if selected_parent_name == "None":
                parent_id = None
            else:
                index = dropdown_names.index(selected_parent_name)
                parent_id = dropdown_ids[index]
            
            self.db.add_category(selected_name, parent_id)
            dialog.destroy()
            self.load_categories()
            
        ctk.CTkButton(dialog, text="Save", command=save).pack(side="left", padx = (100,0), pady = 20)
        ctk.CTkButton(dialog, text="Cancel", command=dialog.destroy).pack(side="right", padx = (0,100), pady = 20)

    def open_edit_category_dialog(self):
        selected = self.tree.selection()
        if len(selected) == 0:
            self.show_warning("Please select a category to edit")
        elif len(selected) > 1:
            self.show_warning("Please select only one category to edit")
        else:
            selected_iid = selected[0]
            values = self.tree.item(selected_iid, "values")
            category_id_being_edited = int(values[0])
            result = self.db.get_category_by_id(category_id_being_edited)
            current_name, current_parent_id = result
            dialog = ctk.CTkToplevel(self)
            dialog.transient(self)
            dialog.grab_set()
            dialog.focus_force()
            dialog.title("Edit Category")
            dialog.geometry("500x300")

            ctk.CTkLabel(dialog, text = "Name: ").pack(pady = 5)
            name_entry = ctk.CTkEntry(dialog)
            name_entry.insert(0, current_name)
            name_entry.pack(pady = 5)

            ctk.CTkLabel(dialog, text = "Parent: ").pack(pady = 5)
            categories = self.db.get_categories()
            dropdown_names = ["None"]
            dropdown_ids = [None]

            for cat_id, name, parent_id in categories:
                if cat_id != category_id_being_edited:
                    dropdown_names.append(name)
                    dropdown_ids.append(cat_id)

            parent_option = ctk.CTkOptionMenu(dialog, values = dropdown_names)
            parent_option.pack(pady = 5)
            if current_parent_id is None:
                parent_option.set("None")
            else:
                index = dropdown_ids.index(current_parent_id)
                parent_option.set(dropdown_names[index])


            def save():
                selected_name = name_entry.get().strip()
                if not selected_name:
                    return
                selected_parent_name = parent_option.get()
                if selected_parent_name == "None":
                    parent_id = None
                else:
                    index = dropdown_names.index(selected_parent_name)
                    parent_id = dropdown_ids[index]

                if parent_id != current_parent_id:
                    if self.db.has_children(category_id_being_edited):
                        confirmed = self.ask_confirmation("This category has subcategories.Moving it will also move them. Continue?")
                        if not confirmed:
                            return

                self.db.update_category(category_id_being_edited, selected_name , parent_id)
                dialog.destroy()
                self.load_categories()

            ctk.CTkButton(dialog, text="Save", command=save).pack(side="left", padx = (100,0), pady = 20)
            ctk.CTkButton(dialog, text="Cancel", command=dialog.destroy).pack(side="right", padx = (0,100), pady = 20)
    
    
    def show_warning(self, message):
        popup = ctk.CTkToplevel(self)
        popup.title("Warning")
        popup.geometry("300x150")
    
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()
    
        label = ctk.CTkLabel(popup, text = message, wraplength = 250)
        label.pack(pady = 20)
        
        def close_popup():
            popup.destroy()
            
        ok_button = ctk.CTkButton(popup, text = "OK", command = close_popup)
        ok_button.pack(pady = 10)
    
    def ask_confirmation(self, message):
        result = [False]
        popup = ctk.CTkToplevel(self)
        popup.title("Warning")
        popup.geometry("300x150")

        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        label = ctk.CTkLabel(popup, text = message, wraplength = 250)
        label.pack(pady = 20)
        
        def confirm():
            result[0] = True
            popup.destroy()
        def close_popup():
            popup.destroy()

        confirm_button = ctk.CTkButton(popup, text = "Confirm", command = confirm)
        confirm_button.pack(pady = 0)
        
        cancel_button = ctk.CTkButton(popup, text = "Cancel", command = close_popup)
        cancel_button.pack(pady = 10)
        
        popup.wait_window()
        return result[0]
    
    

           
        
    
    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = BudgetPlannerApp()
    app.run()

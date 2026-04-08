import customtkinter as ctk
from customtkinter import CTkButton

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
        self.tree.heading("Parent-ID", text="Parent-ID")
        self.tree.column("#0", width=200)
        self.tree.column("ID", width=50)
        self.tree.column("Parent-ID", width=80)
        self.tree.pack(fill="both", expand=True)
        
        frame_buttons = ctk.CTkFrame(self.tab_categories)
        frame_buttons.pack(fill="x", padx = 10, pady = 10)
        
        button_add = CTkButton(frame_buttons, text = "Add")
        button_add.pack(side="left", padx = 5)
        
        button_edit = CTkButton(frame_buttons, text = "Edit")
        button_edit.pack(side="left", padx = 5)
        
        button_del = CTkButton(frame_buttons, text = "Delete")
        button_del.pack(side="left", padx = 5)
        
        self.load_categories()
        
    def load_categories(self):
        self.tree.delete(*self.tree.get_children())
        self.category_map = {}
        rows = self.db.get_all_categories()
        for row in rows:
            category_id, name, parent_id = row
            if parent_id is None:
                tree_id = self.tree.insert("", "end", text=name, values=(category_id, parent_id))
                self.category_map[category_id] = tree_id
                
        for row in rows:
            category_id, name, parent_id = row
            if parent_id is not None:
                parent_tree_id = self.category_map[parent_id]
                tree_id = self.tree.insert(parent_tree_id, "end", text=name, values=(category_id, parent_id))
                self.category_map[category_id] = tree_id            
                
        

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = BudgetPlannerApp()
    app.run()

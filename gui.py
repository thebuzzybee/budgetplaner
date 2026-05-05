import customtkinter as ctk
from customtkinter import CTkButton, CTkToplevel
import CTkCalendar as ctkc
import ctkdateentry as ctkd
from datetime import datetime

from databasemanager import DatabaseManager


class BudgetPlannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Planer")
        self.geometry("750x600")
        self.configure(fg_color = ("SkyBlue1", "SkyBlue4"))
        
        self.db = DatabaseManager()
        self.db.initialize_db()
        self.selected_row = None
        self.selected_category_id = None
        self.selected_subcategory_row = None
        self.current_viewed_parent_id = None
        self.current_selected_child_id = None

        self.create_widgets()
        
    def run(self):
        self.mainloop()
        
    def create_widgets(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        self.tabview.configure(fg_color = ("SkyBlue1", "SkyBlue4"))
        
        self.tab_transactions = self.tabview.add("Transactions")
        self.tab_categories = self.tabview.add("Categories")

        self.left_frame = ctk.CTkFrame(self.tab_categories, width = 200, fg_color = "midnight blue")
        self.left_frame.pack(side="left", fill = "y", padx = 5, pady = 5)
        self.right_container = ctk.CTkFrame(self.tab_categories, fg_color = "transparent")
        self.right_container.pack(side = "left", fill = "both", expand = "True", padx = 5, pady = 5)
        
        self.right_frame = ctk.CTkFrame(self.right_container, fg_color = "midnight blue")
        self.right_frame.pack(side="top", fill = "both", expand = True)
        self.button_bar = ctk.CTkFrame(self.right_container, fg_color = "transparent")
        self.button_bar.pack(side = "bottom", fill = "x", pady = 5)
        
        self.category_view = ctk.CTkScrollableFrame(self.left_frame, 
                                                    label_text = "Your Categories", 
                                                    label_text_color = "LightSkyBlue1", 
                                                    label_fg_color = "RoyalBlue1", 
                                                    scrollbar_button_color = "RoyalBlue1" , 
                                                    scrollbar_button_hover_color = "RoyalBlue4", 
                                                    height = 400, 
                                                    fg_color = "RoyalBlue3")

        self.subcategory_view = ctk.CTkScrollableFrame(self.right_frame,
                                                    label_text = "Subcategories",
                                                    label_text_color = "LightSkyBlue1",
                                                    label_fg_color = "RoyalBlue1",
                                                    scrollbar_button_color = "RoyalBlue1" ,
                                                    scrollbar_button_hover_color = "RoyalBlue4",
                                                    height = 400,
                                                    fg_color = "RoyalBlue3")

        
        
        
        
        button_add = CustomButton(self.button_bar, text = "Add")
        #button_add = CTkButton(self.left_frame, text = "Add Category", width = 140, height = 30, border_width = 2, border_color = "LightSkyBlue1", fg_color = "RoyalBlue3", hover_color = "navy", text_color = "LightSkyBlue1")
        
        button_add.configure(command = self.open_add_category_dialog)
        #button_add.bind("<Enter>", lambda event: button_add.configure(text_color = "alice blue", border_color = "alice blue", fg_color = "navy"))
        #button_add.bind("<Leave>", lambda event: button_add.configure(text_color = "LightSkyBlue1", fg_color = "RoyalBlue3", border_color = "LightSkyBlue1"))
        
        
        self.category_view.pack(side="bottom", fill = "both", expand = True, padx=5, pady = 5)
        self.subcategory_view.pack(side="top", fill = "both", expand = True, padx=5, pady = 5)
        button_add.pack(side="left", padx = 5)
        
        button_edit = CustomButton(self.button_bar, text = "Edit")
        button_edit.pack(side="left", padx = 5)
        button_edit.configure(command = self.open_edit_category_dialog)
        
        button_del = CustomButton(self.button_bar, text = "Delete")
        button_del.pack(side="left", padx = 5)
        button_del.configure(command = self.on_delete_button_click)
        
        self.setup_transactions_tab()
        self.load_categories()

    def setup_transactions_tab(self):
        self.transaction_control_frame = ctk.CTkFrame(self.tab_transactions, fg_color = "transparent")
        self.transaction_control_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        new_transaction_button = CustomButton(self.transaction_control_frame, text = "New Transaction", command = self.open_new_transaction_dialog)
        new_transaction_button.pack(side="left", padx = 5)
        
        self.transaction_overview_frame = ctk.CTkFrame(self.tab_transactions, fg_color = "midnight blue")
        self.transaction_overview_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)
        
        self.transaction_overview = ctk.CTkScrollableFrame(self.transaction_overview_frame, 
                                                                fg_color = "RoyalBlue3", 
                                                                label_text = "Transaction Overview", 
                                                                label_text_color = "alice blue", 
                                                                label_fg_color = "RoyalBlue1",
                                                                scrollbar_button_color = "RoyalBlue1" ,
                                                                scrollbar_button_hover_color = "RoyalBlue4")
        self.transaction_overview.pack(side = "left", expand = True, fill = "both", padx = (0,5), pady = 5)
        self.transaction_detail = ctk.CTkFrame(self.transaction_overview_frame, fg_color = "red")
        self.transaction_detail.pack(side = "right", expand = True, fill = "both", padx = (0,5), pady = 5)
        self.category_segmented_button = ctk.CTkSegmentedButton(self.transaction_overview, 
                                                                values = ["All", "Expense", "Income"], 
                                                                width = 250,
                                                                height = 30,
                                                                fg_color = "RoyalBlue4", 
                                                                selected_color = "RoyalBlue1", 
                                                                selected_hover_color = "navy",
                                                                unselected_color = "LightSkyBlue3",
                                                                unselected_hover_color = "navy",
                                                                text_color = "alice blue", 
                                                                dynamic_resizing = False)
        self.category_segmented_button.set("All")
        self.category_segmented_button.pack(side = "top", padx = 5)
        self.load_transactions()
    def open_new_transaction_dialog(self):
        dialog = CustomTopLevel(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.focus_force()
        dialog.title("New Transaction")
        dialog.geometry("650x420")
        
        
        income_expense_frame = ctk.CTkFrame(dialog, fg_color = "transparent")
        income_expense_frame.pack(fill = "x", pady = 5)
        date_frame = ctk.CTkFrame(dialog, fg_color = "transparent")
        date_frame.pack(fill = "x", pady = 5)
        amount_frame = ctk.CTkFrame(dialog, fg_color = "transparent")
        amount_frame.pack(fill = "x", pady = 5)
        category_frame = ctk.CTkFrame(dialog, fg_color = "transparent")
        category_frame.pack(fill = "x", pady = 5)
        description_frame = ctk.CTkFrame(dialog, fg_color = "transparent")
        description_frame.pack(fill = "x", pady = 5)
       
        self.income_expense_button = ctk.CTkSegmentedButton(income_expense_frame, 
                                                            values = ["Expense", "Income"], 
                                                            width = 250,
                                                            height = 30,
                                                            fg_color = "RoyalBlue4",
                                                            selected_color = "RoyalBlue1",
                                                            selected_hover_color = "navy",
                                                            unselected_color = "LightSkyBlue3",
                                                            unselected_hover_color = "navy",
                                                            text_color = "alice blue",
                                                            dynamic_resizing = False)
        self.income_expense_button.set("Expense")
        self.income_expense_button.pack(padx = 5, pady = 5)
        
        ctk.CTkLabel(date_frame, text = "Date: ", text_color = "alice blue", font = ("Roboto", 20)).pack(side = "left", padx = 20, pady = 10)
        #self.day_entry = ctk.CTkEntry(date_frame, placeholder_text = "DD", width = 35)
        #self.day_entry.pack(side = "left", padx = 5, pady = 10)
        #self.month_entry = ctk.CTkEntry(date_frame, placeholder_text = "MM", width = 40)
        #self.month_entry.pack(side = "left", padx = 5, pady = 10)
        #self.year_entry = ctk.CTkEntry(date_frame, placeholder_text = "YYYY", width = 55)
        #self.year_entry.pack(side = "left", padx = 5, pady = 10)
        ctk.CTkLabel(amount_frame, text = "Amount: ", text_color = "alice blue", font = ("Roboto", 20)).pack(side = "left", padx = 20, pady = 10)
        self.amount_entry = ctk.CTkEntry(amount_frame, placeholder_text = "0,00 €", width = 55)
        self.amount_entry.pack(side = "left", padx = 5, pady = 10)
        ctk.CTkLabel(category_frame, text = "Category: ", text_color = "alice blue", font = ("Roboto", 20)).pack(side = "left", padx = 20, pady = 10)
        
        
        
        
        self.all_cats = self.db.get_all_categories()
        
        self.parent_names = ["Select Parent"]
        self.parent_ids = [None]
        for cat_id, name, parent_id in self.all_cats:
            if parent_id is None:
                self.parent_names.append(name)
                self.parent_ids.append(cat_id)
                
        self.children_names = ["Select Subcategory"]
        self.children_ids = [None]
        self.grandchildren_names = ["Select Sub-Subcategory"]
        self.grandchildren_ids = [None]
        
        self.final_cat_id = None
        
        def on_parent_change(selected_name):
            if selected_name == "Select Parent":
                return
            index = self.parent_names.index(selected_name)
            selected_parent_id = self.parent_ids[index]
            
            self.children_names = ["Select Subcategory"]
            self.children_ids = [None]
            
            for cat_id, name, row_parent_id in self.all_cats:
                if row_parent_id == selected_parent_id:
                    self.children_names.append(name)
                    self.children_ids.append(cat_id)
                    
            children_dropdown.configure(values = self.children_names)
            children_dropdown.set("Select Subcategory")
            
            if len(self.children_names) > 1:
                children_dropdown.configure(state = "normal")
            else:
                children_dropdown.configure(state = "disabled")
                
            self.final_cat_id = None
        def on_child_change(selected_name):
            index = self.children_names.index(selected_name)
            selected_child_id = self.children_ids[index]
            
            self.grandchildren_names = ["Select Sub-Subcategory"]
            self.grandchildren_ids = [None]
            
            for cat_id, name, row_parent_id in self.all_cats:
                if row_parent_id == selected_child_id:
                    self.grandchildren_names.append(name)
                    self.grandchildren_ids.append(cat_id)
                    
            grandchildren_dropdown.configure(values = self.grandchildren_names)
            grandchildren_dropdown.set("Select Sub-Subcategory")
            
            if len(self.grandchildren_names) > 1:
                grandchildren_dropdown.configure(state = "normal")
            else:
                grandchildren_dropdown.configure(state = "disabled")
            
            self.final_cat_id = None
        
        
        def on_grandchild_change(selected_name):
            index = self.grandchildren_names.index(selected_name)
            self.final_cat_id = self.grandchildren_ids[index]
            
        parent_dropdown = ctk.CTkOptionMenu(category_frame, values = self.parent_names, command = on_parent_change, width = 140)
        parent_dropdown.pack(side="left", padx=5, pady=5)
        parent_dropdown.set(self.parent_names[0])
        
        children_dropdown = ctk.CTkOptionMenu(category_frame, values = self.children_names, command = on_child_change, width = 140, state = "disabled")
        children_dropdown.pack(side="left", padx=5, pady=5)
        children_dropdown.set(self.children_names[0])
        
        grandchildren_dropdown = ctk.CTkOptionMenu(category_frame, values = self.grandchildren_names, command = on_grandchild_change, width = 140, state = "disabled")
        grandchildren_dropdown.pack(side="left", padx=5, pady=5)
        grandchildren_dropdown.set(self.grandchildren_names[0])
        
        self.date_entry = ctkd.CTkDateEntry(date_frame, width = 140)
        self.date_entry.pack(side="left", padx=5, pady=5)


        ctk.CTkLabel(description_frame, text = "Description: ", text_color = "alice blue", font = ("Roboto", 20)).pack(side = "left", padx = 20, pady = 10)
        self.description_entry = ctk.CTkEntry(description_frame, placeholder_text = "Description")
        self.description_entry.pack(side="left", expand = True, fill = "x", padx=5, pady=5)
            
        def save():
            raw_date = self.date_entry.entry.get()
            
            try:
                formatted_date = datetime.strptime(raw_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                self.show_warning("Invalid date. Please pick from the calendar.")
                return
                
            raw_amount = self.amount_entry.get().strip().replace(" €", "")
            raw_amount = raw_amount.replace(",", ".")
            
            try:
                raw_amount = float(raw_amount)
                if raw_amount < 0:
                    self.show_warning("Amount must be a positive number.")
                    return
            except ValueError:
                self.show_warning("Amount must be a number.")
                return
            
            if self.final_cat_id is None:
                self.show_warning("Please select a category.")
                return
                
            raw_type = self.income_expense_button.get()
            raw_description = self.description_entry.get() or None
            self.db.add_transaction(formatted_date, raw_amount, raw_type, self.final_cat_id, raw_description)
            self.load_transactions()
            dialog.destroy()
        
        CustomButton(dialog, text="Save", command=save).pack(side="left", padx = (100,0), pady = 20)
        CustomButton(dialog, text="Cancel", command=dialog.destroy).pack(side="right", padx = (0,100), pady = 20)
    
    
    def load_transactions(self):
        for widget in self.transaction_overview.winfo_children():
            widget.destroy()
            
        roots = self.db.get_transactions()
        print(roots)
        for _, date, amount, transaction_type, category_id, _ in roots:
            row = ctk.CTkButton(
                self.transaction_overview,
                text=f" {category_id} | {date} | {transaction_type} | {amount:.2f}",
                anchor="w",
                fg_color="transparent",
                hover_color="RoyalBlue1",
                text_color="alice blue",
                height=35
            )
            row.pack(fill="x", pady=2)
        
        
            
        
        
        
    
    def _build_category_tree(self):
        flat_list = self.db.get_all_categories()
        tree_dict = {}
        for cat_id, name, parent_id in flat_list:
            tree_dict.setdefault(parent_id, []).append((cat_id, name))
        return tree_dict
        
                
        

    def load_categories(self):
        for widget in self.category_view.winfo_children():
            widget.destroy()

        self.selected_row = None
        self.category_tree = self._build_category_tree()
        roots = self.category_tree.get(None, [])
    
        for cat_id, name in roots:
            row = ctk.CTkButton(
                self.category_view,
                text=name,
                anchor="w",
                fg_color="transparent",
                hover_color="RoyalBlue1",
                text_color="alice blue",
                height=35
            )
            row.pack(fill="x", pady=2)

            if cat_id == self.current_viewed_parent_id:
                row.configure(fg_color="RoyalBlue1")
                self.selected_row = row
                self.selected_category_id = cat_id
    
            row.configure(command=lambda cid=cat_id, btn=row: self.on_parent_click(cid, btn))

    def on_parent_click(self, category_id, button):
        self.selected_subcategory_row = None
        if self.selected_row is not None:
            self.selected_row.configure(fg_color="transparent")
    
        button.configure(fg_color="RoyalBlue1")
        self.selected_row = button
        self.selected_category_id = category_id
    
        
        self.show_category_detail(category_id)
    
    def show_category_detail(self, category_id):
        self.current_viewed_parent_id = category_id
        self.selected_subcategory_row = None
        for widget in self.right_frame.winfo_children():
            widget.destroy()
    
        result = self.db.get_category_by_id(category_id)
        if not result:
            return
        name, parent_id = result
    
        header = ctk.CTkFrame(self.right_frame, fg_color="RoyalBlue2")
        header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(header, text=name, font=("Roboto", 24, "bold"), text_color="alice blue").pack(pady=15)
    
        ctk.CTkLabel(self.right_frame, text="Subcategories:", text_color = "alice blue",font=("Roboto", 14, "bold")).pack(anchor="w", padx=10, pady=(10,5))
    
        children = self.category_tree.get(category_id, [])
    
        if not children:
            ctk.CTkLabel(self.right_frame, text="No subcategories", text_color="alice blue").pack(padx=20)
        else:
            for child_id, child_name in children:
                self._show_child_row(child_id, child_name, indent=0)

    def _show_child_row(self, category_id, name, indent=0):
        left_pad = 20 + (indent * 20)

        row = ctk.CTkButton(
            self.right_frame,
            text=name,
            anchor="w",
            fg_color="transparent",
            hover_color="RoyalBlue2",
            text_color="white",
            height=25
        )
        row.pack(fill="x", padx=(left_pad, 20), pady=1)
    
        row.configure(command=lambda cid=category_id, btn=row: self.on_subcategory_click(cid, btn))
    
        grandchildren = self.category_tree.get(category_id, [])
        for grandchild_id, grandchild_name in grandchildren:
            self._show_child_row(grandchild_id, grandchild_name, indent=indent+1)

    def on_subcategory_click(self, category_id, button):
        if self.selected_subcategory_row is not None:
            self.selected_subcategory_row.configure(fg_color="transparent")
    
        button.configure(fg_color="RoyalBlue1")
        self.selected_subcategory_row = button
        self.selected_category_id = category_id
     
    def open_add_category_dialog(self):
        dialog = CustomTopLevel(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.focus_force()
        dialog.title("Add Category")
        dialog.geometry("500x320")
        
        ctk.CTkLabel(dialog, text = "Name: ", text_color = "alice blue", font = ("Roboto", 20)).pack(pady = 5)
        name_entry = ctk.CTkEntry(dialog)
        name_entry.pack(pady = 5)
        
        ctk.CTkLabel(dialog, text = "Parent: ", text_color = "alice blue", font = ("Roboto", 20)).pack(pady = 5)
        categories = self.db.get_categories()
        dropdown_names = ["None"]
        dropdown_ids = [None]
        
        for category_id, name, parent_id in categories:
            dropdown_names.append(name)
            dropdown_ids.append(category_id)


        def on_parent_selected(selected_parent_name):
            index = dropdown_names.index(selected_parent_name)
            parent_id = dropdown_ids[index]
            
            self.child_names = ["None"]
            self.child_ids = [None]
            
            if self.db.has_children(parent_id):
                children = self.db.get_children(parent_id)
                
                for cat_id, name in children:
                    self.child_names.append(name)
                    self.child_ids.append(cat_id)
                child_option.configure(values=self.child_names, state="normal")
                child_option.set("None")
            else:
                child_option.configure(values=["None"], state="disabled")
                child_option.set("None")
                    
              
        parent_option = ctk.CTkOptionMenu(dialog, values = dropdown_names, command = on_parent_selected)
        parent_option.pack(pady = 5)

        ctk.CTkLabel(dialog, text = "Subcategory: ", text_color = "alice blue", font = ("Roboto", 20)).pack(pady = 10)
        
        child_option = ctk.CTkOptionMenu(dialog, values=["None"], state = "disabled")
        child_option.set("None")
        child_option.pack(pady = 5)

        if self.current_viewed_parent_id is not None:
            if self.current_viewed_parent_id in dropdown_ids:
                index = dropdown_ids.index(self.current_viewed_parent_id)
                parent_name = dropdown_names[index]
                parent_option.set(parent_name)
                on_parent_selected(parent_name)
        
                if self.selected_category_id in self.child_ids:
                    
                    child_index = self.child_ids.index(self.selected_category_id)
                    child_option.set(self.child_names[child_index])
                
        def save():
            selected_name = name_entry.get().strip()
            if not selected_name:
                return
            selected_parent_name = parent_option.get()
            if selected_parent_name == "None":
                parent_id = None
            else:
                if child_option.get() == "None" or child_option.cget("state") == "disabled":
                    index = dropdown_names.index(selected_parent_name)
                    parent_id = dropdown_ids[index]
                else:
                    index = self.child_names.index(child_option.get())
                    parent_id = self.child_ids[index]
                    
            
            self.db.add_category(selected_name, parent_id)
            dialog.destroy()
            self.load_categories()

            if self.current_viewed_parent_id:
                self.show_category_detail(self.current_viewed_parent_id)
            
        CustomButton(dialog, text="Save", command=save).pack(side="left", padx = (100,0), pady = 20)
        CustomButton(dialog, text="Cancel", command=dialog.destroy).pack(side="right", padx = (0,100), pady = 20)

    def open_edit_category_dialog(self):
        if self.selected_category_id is None:
            self.show_warning("Please select a category to edit")
            return
    
        category_id_being_edited = self.selected_category_id
        result = self.db.get_category_by_id(category_id_being_edited)
        if not result:
            return
    
        current_name, current_parent_id = result
        dialog = ctk.CTkToplevel(self, fg_color = "RoyalBlue3")
        dialog.transient(self)
        dialog.grab_set()
        dialog.focus_force()
        dialog.title("Edit Category")
        dialog.geometry("500x350")

        ctk.CTkLabel(dialog, text = "Name: ", text_color = "alice blue", font = ("Roboto", 20)).pack(pady = 5)
        name_entry = ctk.CTkEntry(dialog)
        name_entry.insert(0, current_name)
        name_entry.pack(pady = 5)

        ctk.CTkLabel(dialog, text = "Parent: ", text_color = "alice blue", font = ("Roboto", 20)).pack(pady = 5)
        categories = self.db.get_categories()
        dropdown_names = ["None"]
        dropdown_ids = [None]

        for category_id, name, parent_id in categories:
            if category_id != category_id_being_edited:
                dropdown_names.append(name)
                dropdown_ids.append(category_id)

        def on_parent_selected(selected_parent_name):
            index = dropdown_names.index(selected_parent_name)
            parent_id = dropdown_ids[index]
            
            self.child_names = ["None"]
            self.child_ids = [None]
            
            if self.db.has_children(parent_id):
                children = self.db.get_children(parent_id)
                for cat_id, name in children:
                    if cat_id != category_id_being_edited:
                        self.child_names.append(name)
                        self.child_ids.append(cat_id)

                child_option.configure(values=self.child_names, state="normal")
                child_option.set("None")

            else:
                child_option.configure(values=["None"], state="disabled")
                child_option.set("None")

            print(f"Selected parent: {selected_parent_name}")


        parent_option = ctk.CTkOptionMenu(dialog, values = dropdown_names, command = on_parent_selected)
        parent_option.pack(pady = 5)

        ctk.CTkLabel(dialog, text = "Subcategory: ", text_color = "alice blue", font = ("Roboto", 20)).pack(pady = 10)

        child_option = ctk.CTkOptionMenu(dialog, state = "disabled")
        child_option.set("None")
        child_option.pack(pady = 5)

        if current_parent_id is None:
            parent_option.set("None")
            child_option.configure(state="disabled")
        else:
        
            if current_parent_id in dropdown_ids:
                index = dropdown_ids.index(current_parent_id)
                root_name = dropdown_names[index]
                parent_option.set(root_name)
                on_parent_selected(root_name)
                child_option.set("None")
            else:
                root_id = self.db.get_root_ancestor(current_parent_id)                
                root_index = dropdown_ids.index(root_id)
                root_name = dropdown_names[root_index]
                parent_option.set(root_name)
                on_parent_selected(root_name)
                if current_parent_id in self.child_ids:
                    child_index = self.child_ids.index(current_parent_id)
                    child_option.set(self.child_names[child_index])
        def save():
            selected_name = name_entry.get().strip()
            if not selected_name:
                return
            selected_parent_name = parent_option.get()
            if selected_parent_name == "None":
                new_parent_id = None
            else:
                if child_option.get() == "None" or child_option.cget("state") == "disabled":
                    index = dropdown_names.index(selected_parent_name)
                    new_parent_id = dropdown_ids[index]
                else:
                    index = self.child_names.index(child_option.get())
                    new_parent_id = self.child_ids[index]
            if new_parent_id != current_parent_id:  
                if self.db.has_children(category_id_being_edited):
                    self.show_warning("Cannot move: category has subcategories. Delete or move subcategories first.")
                    return

            self.db.update_category(category_id_being_edited, selected_name, new_parent_id)
            dialog.destroy()
            self.load_categories()

            if self.current_viewed_parent_id:
                self.show_category_detail(self.current_viewed_parent_id)

        CustomButton(dialog, text="Save", command=save).pack(side="left", padx = (100,0), pady = 20)
        CustomButton(dialog, text="Cancel", command=dialog.destroy).pack(side="right", padx = (0,100), pady = 20)


    def on_delete_button_click(self):
        if self.selected_category_id is None:
            self.show_warning("Please select a category to delete")
            return
    
        category_id = self.selected_category_id

        result = self.db.get_category_by_id(category_id)
        name = result[0]

        total = self.db.count_descendants(category_id)

        if total == 1:
            message = f"Delete '{name}'?"
        else:
            message = f"Delete '{name}' and {total-1} subcategories?"
    

        confirmed = self.ask_confirmation(message)
    
        if confirmed:
            self.db.delete_category_recursive(category_id)
            self.selected_row = None
            self.selected_category_id = None
            self.load_categories()

            if self.current_viewed_parent_id:
                self.show_category_detail(self.current_viewed_parent_id)
    
    def show_warning(self, message):
        popup = CustomTopLevel(self)
        popup.title("Warning")
        popup.geometry("300x150")
    
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()
    
        label = ctk.CTkLabel(popup, text = message, text_color = "alice blue", font = ("Roboto", 15), wraplength = 250)
        label.pack(pady = 20)
        
        def close_popup():
            popup.destroy()
            
        ok_button = CustomButton(popup, text = "OK", command = close_popup)
        ok_button.pack(pady = 10)
    
    def ask_confirmation(self, message):
        result = [False]
        popup = CustomTopLevel(self)
        popup.title("Warning")
        popup.geometry("300x150")

        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        label = ctk.CTkLabel(popup, text = message, text_color = "alice blue", font = ("Roboto", 15), wraplength = 250)
        label.pack(pady = 20)
        
        def confirm():
            result[0] = True
            popup.destroy()
        def close_popup():
            popup.destroy()

        confirm_button = CustomButton(popup, text = "Confirm", command = confirm)
        confirm_button.pack(pady = 0)
        
        cancel_button = CustomButton(popup, text = "Cancel", command = close_popup)
        cancel_button.pack(pady = 10)
        
        popup.wait_window()
        return result[0]
    
class CustomButton(ctk.CTkButton):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(width = 140,
                    height = 30,
                    border_width = 2,
                    border_color = "LightSkyBlue1",
                    fg_color = "RoyalBlue3",
                    text_color = "LightSkyBlue1")
        
        def on_enter(event):
            self.configure(text_color = "alice blue", border_color = "alice blue", fg_color = "navy")
            
        def on_leave(event):
            self.configure(text_color = "LightSkyBlue1", fg_color = "RoyalBlue3", border_color = "LightSkyBlue1")
            
        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)
    
class CustomTopLevel(ctk.CTkToplevel):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color = "midnight blue")

if __name__ == "__main__":
    app = BudgetPlannerApp()
    app.run()

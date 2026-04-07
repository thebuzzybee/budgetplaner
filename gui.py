import customtkinter as ctk

class BudgetPlannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Planer")
        self.geometry("1000x600")

        self.create_widgets()

    def create_widgets(self):
        label = ctk.CTkLabel(self, text="Budget Planer – GUI wird aufgebaut")
        label.pack(pady=20)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = BudgetPlannerApp()
    app.run()

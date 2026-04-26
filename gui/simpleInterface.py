import customtkinter as ctk
from src.models import LPProblemModel

class SimpleInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LP Solver - Objective Function")
        self.geometry("600x400")
        self.model = LPProblemModel()
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.main_frame, text="Enter the number of variables:")
        self.label.pack(pady=(10, 5))
        
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text="e.g., 3")
        self.entry.pack(pady=5)
        
        self.button = ctk.CTkButton(self.main_frame, text="Generate Objective Row", command=self.get_input)
        self.button.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(self.main_frame, text="", text_color="red")
        self.status_label.pack(pady=5)

        self.obj_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.obj_frame.pack(pady=20)

    def get_input(self):
        user_input = self.entry.get()
        try:
            val = int(user_input)
            if val > 0:
                returned = self.model.set_num_vars(val)
                self.status_label.configure(text=f"Variables set to: {returned}", text_color="green")
                self.create_objective_row(val)
            else:
                self.status_label.configure(text="Please enter a positive integer.", text_color="red")
        except ValueError:
            self.status_label.configure(text="Invalid input.", text_color="red")

    def create_objective_row(self, n):
        for widget in self.obj_frame.winfo_children():
            widget.destroy()

        self.opt_type = ctk.CTkOptionMenu(self.obj_frame, values=["Max", "Min"], width=80)
        self.opt_type.grid(row=0, column=0, padx=5)

        ctk.CTkLabel(self.obj_frame, text="Z = ").grid(row=0, column=1, padx=2)

        self.obj_entries = []
        for i in range(n):
            entry = ctk.CTkEntry(self.obj_frame, width=50)
            entry.grid(row=0, column=2 + (i*2), padx=2)
            self.obj_entries.append(entry)

            var_text = f"x{i+1}" + (" + " if i < n-1 else "")
            ctk.CTkLabel(self.obj_frame, text=var_text).grid(row=0, column=3 + (i*2), padx=2)


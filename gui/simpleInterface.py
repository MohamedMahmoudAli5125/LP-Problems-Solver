# import customtkinter as ctk
# from src.models import LPProblemModel

# class SimpleInterface(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("LP Solver - Objective Function")
#         self.geometry("800x600")
#         self.model = LPProblemModel()
        
#         self.num_vars = 0 
#         self.all_constraints_widgets = [] 
#         self.var_type_widgets = []
        
#         self.main_frame = ctk.CTkScrollableFrame(self)
#         self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

#         self.label = ctk.CTkLabel(self.main_frame, text="Enter the number of variables:")
#         self.label.pack(pady=(10, 5))
        
#         self.entry = ctk.CTkEntry(self.main_frame, placeholder_text="e.g., 3")
#         self.entry.pack(pady=5)
        
#         self.button = ctk.CTkButton(self.main_frame, text="Generate Objective Row", command=self.get_input)
#         self.button.pack(pady=10)
        
#         self.status_label = ctk.CTkLabel(self.main_frame, text="", text_color="red")
#         self.status_label.pack(pady=5)

#         self.obj_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
#         self.obj_frame.pack(pady=20)
        
#         self.constraints_label = ctk.CTkLabel(self.main_frame, text="Constraints:")
#         self.constraints_label.pack(pady=(0, 5), anchor="w")
#         self.constraints_label.pack_forget() 

       
#         self.constraints_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
#         self.constraints_frame.pack(pady=10 , fill="both", expand=True)
         
#         self.addConstraints_button = ctk.CTkButton(self.main_frame, text="Add Constraints", command=self.add_constraint_row , state="disabled" , width=120)        
#         self.addConstraints_button.pack(pady=10)

#         self.bounds_label = ctk.CTkLabel(self.main_frame, text="Variable Bounds:", font=("Arial", 14, "bold"))
#         self.bounds_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
#         self.solve_button = ctk.CTkButton(self.main_frame, text="Solve & Print Model", 
#                                          fg_color="green", hover_color="darkgreen",
#                                          command=self.extract_data_to_model)
#         self.solve_button.pack(side="bottom", pady=20)
#     def get_input(self):
        
#         try:
#             self.num_vars = int(self.entry.get())
#             if self.num_vars <= 0:
#                 raise ValueError
#             self.status_label
            
#             self.status_label.configure(text="Ready to create objective function.", text_color="green")
#             self.addConstraints_button.configure(state="normal")
            
        
#             self.create_objective_row()
#             self.create_bounds_section()
            
#             self.constraints_label.pack(pady=(0, 5), anchor="w", before=self.constraints_frame)

            
#             for child in self.constraints_frame.winfo_children():
#                 child.destroy()
#             self.all_constraints_widgets = []
#         except ValueError:
#             self.status_label.configure(text="Please enter a valid positive integer.", text_color="red")

#     def create_bounds_section(self):
#         for child in self.bounds_frame.winfo_children():
#             child.destroy()
#         self.var_type_widgets = []

#         self.bounds_label.pack(pady=(20, 5))
#         self.bounds_frame.pack(pady=5, fill="x")

#         for i in range(self.num_vars):
#             container = ctk.CTkFrame(self.bounds_frame, fg_color="transparent")
#             container.pack(side="left", padx=10)
            
#             ctk.CTkLabel(container, text=f"x{i+1}:").pack(side="left", padx=2)
#             menu = ctk.CTkOptionMenu(container, values=["≥ 0", "Unrestricted"], width=110)
#             menu.set("≥ 0") 
#             menu.pack(side="left")
#             self.var_type_widgets.append(menu)
#     def create_objective_row(self):
#         for widget in self.obj_frame.winfo_children():
#             widget.destroy()

#         self.opt_type = ctk.CTkOptionMenu(self.obj_frame, values=["Max", "Min"], width=80)
#         self.opt_type.grid(row=0, column=0, padx=5)

#         ctk.CTkLabel(self.obj_frame, text="Z = ").grid(row=0, column=1, padx=2)

#         self.obj_entries = []
#         for i in range(self.num_vars):
#             entry = ctk.CTkEntry(self.obj_frame, width=50)
#             entry.grid(row=0, column=2 + (i*2), padx=2)
#             self.obj_entries.append(entry)

#             var_text = f"x{i+1}" + (" + " if i < self.num_vars-1 else "")
#             ctk.CTkLabel(self.obj_frame, text=var_text).grid(row=0, column=3 + (i*2), padx=2)
            

#     def add_constraint_row(self):
#         row_idx = len(self.all_constraints_widgets)
#         row_frame = ctk.CTkFrame(self.constraints_frame, fg_color="transparent")
#         row_frame.pack(pady=5, anchor="center")

#         current_row_entries = []

#         for i in range(self.num_vars):
#             entry = ctk.CTkEntry(row_frame, width=50)
#             entry.grid(row=0, column=i*2, padx=2)
#             current_row_entries.append(entry)

#             var_text = f"x{i+1}" + (" + " if i < self.num_vars - 1 else "")
#             ctk.CTkLabel(row_frame, text=var_text).grid(row=0, column=1 + i*2 , padx=2)

#         op_menu = ctk.CTkOptionMenu(row_frame, values=["≤", "≥", "="], width=60)
#         op_menu.grid(row=0, column=self.num_vars*2, padx=10)
        
#         rhs_entry = ctk.CTkEntry(row_frame, width=60, placeholder_text="RHS")
#         rhs_entry.grid(row=0, column=self.num_vars*2 + 1, padx=2)
        
#         delete_btn = ctk.CTkButton(row_frame, text="X", width=30, fg_color="#CC3333", 
#                                    hover_color="#AA2222", 
#                                    command=lambda rf=row_frame: self.delete_row(rf))
#         delete_btn.grid(row=0, column=self.num_vars*2 + 2, padx=10)
        
#         row_data = {
#             "frame": row_frame,
#             "entries": current_row_entries,
#             "op": op_menu,
#             "rhs": rhs_entry
#         }
#         self.all_constraints_widgets.append(row_data)
        
        
#     def delete_row(self, frame_to_delete):
#         self.all_constraints_widgets = [
#             r for r in self.all_constraints_widgets if r["frame"] != frame_to_delete
#         ]
#         frame_to_delete.destroy()
        
#     def extract_data_to_model(self):
#         try:
#             self.model.num_vars = self.num_vars
#             self.model.obj_type = self.opt_type.get()
#             self.model.var_types = [v.get() for v in self.var_type_widgets]
#             self.model.obj_coeffs = [float(e.get() if e.get() else 0) for e in self.obj_entries]
            
#             self.model.constraints_matrix = []
#             self.model.rhs_list = []
#             self.model.operators = []
            
#             for row in self.all_constraints_widgets:
#                 coeffs = [float(e.get() if e.get() else 0) for e in row["entries"]]
#                 self.model.constraints_matrix.append(coeffs)
                
#                 self.model.rhs_list.append(float(row["rhs"].get() if row["rhs"].get() else 0))
#                 self.model.operators.append(row["op"].get())

#             self.print_model_summary()
#             self.status_label.configure(text="Data extracted successfully!", text_color="green")
#             from src.standardizer import Standardizer 
            
#             standardizer = Standardizer(self.model)
#             std_output = standardizer.standardize()
            
#             self.print_standardized_results(std_output)
#             self.status_label.configure(text="Standardization complete! Check console for details.", text_color="green")
            
#         except ValueError:
#             self.status_label.configure(text="Error: Please ensure all coefficients are numbers.", text_color="red")

#     def print_model_summary(self):
#         print("--- LP MODEL SUMMARY ---")
#         print(f"Type: {self.model.obj_type}")
#         print(f"Objective: {self.model.obj_coeffs}")
#         print("Constraints:")
#         for i in range(len(self.model.constraints_matrix)):
#             print(f"  {self.model.constraints_matrix[i]} {self.model.operators[i]} {self.model.rhs_list[i]}")
#         print(f"Variable Types: {self.model.var_types}")
#     def print_standardized_results(self, out):
#         print("\n=== STANDARDIZED TABLEAU DATA ===")
#         print(f"Metadata: {out.col_metaData}")
#         print(f"Matrix A:\n{out.A}")
#         print(f"RHS (b): {out.b}")
#         print(f"Phase 1 Obj: {out.phase1_obj}")
#         print(f"Phase 2 Obj: {out.phase2_obj}")
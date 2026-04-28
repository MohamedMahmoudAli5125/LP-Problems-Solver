import customtkinter as ctk
from gui.input_frame import InputFrame
from gui.output_frame import OutputFrame

class LPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("LP Solver - Split Interface")
        self.geometry("1100x700")

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.output_section = OutputFrame(self, corner_radius=0)
        self.output_section.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.input_section = InputFrame(self, output_ref=self.output_section, corner_radius=0)
        self.input_section.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


import customtkinter as ctk
from gui.input_frame import InputFrame
from gui.output_frame import OutputFrame
import tkinter as tk

class LPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("LP Solver - Split Interface")
        self.geometry("1100x700")

        # self.grid_columnconfigure(0, weight=1) 
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_rowconfigure(0, weight=1)

        # self.output_section = OutputFrame(self, corner_radius=0)
        # self.output_section.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # self.input_section = InputFrame(self, output_ref=self.output_section, corner_radius=0)
        # self.input_section.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
 
        self.paned = tk.PanedWindow(
            self,
            orient=tk.HORIZONTAL,
            sashwidth=6,
            sashrelief="flat",
            bg="#888787",
            bd=0,
        )
        self.paned.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
 
        left_wrapper = tk.Frame(self.paned, bd=0)
        right_wrapper = tk.Frame(self.paned, bd=0)
 
        self.output_section = OutputFrame(right_wrapper, corner_radius=0)
        self.input_section = InputFrame(left_wrapper, output_ref=self.output_section, corner_radius=0)
 
        self.input_section.pack(fill="both", expand=True)
        self.output_section.pack(fill="both", expand=True)
 
        self.paned.add(left_wrapper,  minsize=280, stretch="always")
        self.paned.add(right_wrapper, minsize=280, stretch="always")
import customtkinter as ctk
from tkinter import filedialog


class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.textbox = ctk.CTkTextbox(
            self,
            font=("Courier New", 12),
            wrap="none",
            state="disabled"
        )
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)

        self._full_text = ""

    def display_result(self, trace_string: str):
        self._full_text = trace_string
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", trace_string)
        self.textbox.configure(state="disabled")

    def display_ok(self):
        self.display_result("Solve complete.")
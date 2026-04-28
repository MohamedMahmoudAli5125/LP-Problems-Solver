import customtkinter as ctk

class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label = ctk.CTkLabel(self, text="Output Section", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)
        
        self.result_text = ctk.CTkLabel(self, text="Results will appear here...", text_color="gray")
        self.result_text.pack(expand=True)

    def display_ok(self):
        self.result_text.configure(text="OK", text_color="green", font=("Arial", 24, "bold"))
import customtkinter as ctk


class RegisterTitle(ctk.CTkLabel):
    def __init__(self, master):
        super().__init__(master, text="Crea il tuo account", font=("Arial", 24, "bold"))
        self.grid(row=0, column=0, columnspan=2, pady=(20, 40))

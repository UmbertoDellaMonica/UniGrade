import customtkinter as ctk


class RememberCheckbox(ctk.CTkCheckBox):
    def __init__(self, master, variable):
        super().__init__(master, text="Ricordami", variable=variable)

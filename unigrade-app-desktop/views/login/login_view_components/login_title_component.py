import customtkinter as ctk
from configuration.unigrade_configuration import APP_NAME


class LoginTitle(ctk.CTkLabel):
    def __init__(self, master):
        super().__init__(master, text=f"{APP_NAME}", font=("Arial", 36, "bold"))

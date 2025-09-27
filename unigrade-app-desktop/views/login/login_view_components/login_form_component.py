import customtkinter as ctk


class LoginForm(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.entry_matricola = ctk.CTkEntry(
            self, placeholder_text="Matricola", width=300
        )
        self.entry_matricola.pack(pady=10)
        self.entry_password = ctk.CTkEntry(
            self, placeholder_text="Password", show="*", width=300
        )
        self.entry_password.pack(pady=10)

import customtkinter as ctk


class FormEntry(ctk.CTkFrame):
    def __init__(self, master, labels):
        super().__init__(master)
        self.entries = {}
        for i, lbl in enumerate(labels):
            ctk.CTkLabel(self, text=lbl, font=("Arial", 14)).grid(
                row=i, column=0, sticky="e", padx=(20, 10), pady=10
            )
            ent = ctk.CTkEntry(self, show="*" if "Password" in lbl else None, width=250)
            ent.grid(row=i, column=1, sticky="w", padx=(10, 20), pady=10)
            self.entries[lbl] = ent

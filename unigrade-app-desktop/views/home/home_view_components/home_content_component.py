import customtkinter as ctk


class HomeContent(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=20, fg_color="#2e2e3e")
        self.pack(side="right", expand=True, fill="both", padx=25, pady=25)

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

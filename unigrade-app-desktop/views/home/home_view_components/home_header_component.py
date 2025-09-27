import customtkinter as ctk


class HomeHeader(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent", height=50)
        self.pack(fill="x", pady=(0, 15))

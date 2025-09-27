import customtkinter as ctk


class HomeSidebar(ctk.CTkFrame):
    def __init__(self, master, buttons):
        super().__init__(master, width=220, corner_radius=0, fg_color="#11111b")
        self.pack(side="left", fill="y", pady=20)

        for text, cmd in buttons:
            ctk.CTkButton(
                self,
                text=text,
                command=cmd,
                anchor="w",
                height=60,
                corner_radius=15,
                font=("Arial", 16, "bold"),
                fg_color="#1a1a2e",
                hover_color="#33334d",
            ).pack(fill="x", pady=10, padx=15)

import customtkinter as ctk


class CourseDropdown(ctk.CTkFrame):
    def __init__(
        self, master, label="Corso di Laurea", options=None, default="Triennale"
    ):
        super().__init__(master)
        if options is None:
            options = ["Triennale", "Magistrale"]

        self.var = ctk.StringVar(value=default)

        # Label più piccola e padding ridotto
        ctk.CTkLabel(self, text=label, font=("Arial", 12)).grid(
            row=0, column=0, sticky="e", padx=(10, 5), pady=5
        )

        # Dropdown ridotto in larghezza e padding più piccolo
        ctk.CTkOptionMenu(
            self,
            values=options,
            variable=self.var,
            width=180,
            height=28,
            corner_radius=8,
            fg_color="#1f6aa5",  # colore del pulsante (opzionale)
            dropdown_fg_color="#ffffff",  # sfondo lista a tendina
            dropdown_text_color="#000000",  # colore testo voci
            button_color="#1f6aa5",  # colore pulsante (facoltativo)
            button_hover_color="#aaaaaa",  # hover pulsante
        ).grid(row=0, column=1, sticky="w", padx=(5, 10), pady=5)

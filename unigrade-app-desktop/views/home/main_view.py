import customtkinter as ctk
from configuration.unigrade_configuration import set_app_icon
from configuration.unigrade_token_configuration import clear_token


class MainView:
    def __init__(self, master, student_id):
        self.master = master
        self.student_id = student_id

        # --- Container principale della MainView ---
        self.container = ctk.CTkFrame(master)
        self.container.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self.container, width=220, corner_radius=0, fg_color="#11111b"
        )
        self.sidebar.pack(side="left", fill="y", pady=20)

        # Content
        self.content = ctk.CTkFrame(
            self.container, corner_radius=20, fg_color="#2e2e3e"
        )
        self.content.pack(side="right", expand=True, fill="both", padx=25, pady=25)

        # Header frame per icona refresh (se vuoi usarlo nella content)
        self.header_frame = ctk.CTkFrame(
            self.content, fg_color="transparent", height=50
        )
        self.header_frame.pack(fill="x", pady=(0, 15))

        # Sidebar buttons
        buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📚 Libretto", self.show_libretto),
            ("🚪 Logout", self.logout),
        ]

        for text, cmd in buttons:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                command=cmd,
                anchor="w",
                height=60,
                corner_radius=15,
                font=("Arial", 16, "bold"),
                fg_color="#1a1a2e",
                hover_color="#33334d",
            ).pack(fill="x", pady=10, padx=15)

        # Mostra la dashboard di default
        self.show_dashboard()

    def show_dashboard(self):
        from views.main_sub_view.dashboard_view import DashboardView

        # Pulisce il contenuto prima di mostrare la nuova view
        for w in self.content.winfo_children():
            w.destroy()
        dashboard = DashboardView(self.content, self.student_id)
        dashboard.pack(fill="both", expand=True)  # <-- questa è la chiave

    def show_libretto(self):
        from views.main_sub_view.libretto_view import LibrettoView

        for w in self.content.winfo_children():
            w.destroy()
        LibrettoView(self.content, self.student_id)

    def logout(self):
        # Finestra modale
        modal = ctk.CTkToplevel(self.master)
        modal.title("Conferma Logout")
        modal.geometry("450x270")
        modal.grab_set()
        modal.resizable(False, False)
        set_app_icon(modal)

        # Titolo
        ctk.CTkLabel(
            modal,
            text="⚠️ Sei sicuro di voler uscire?",
            font=("Arial", 22, "bold"),
            text_color="#ff5555",
        ).pack(pady=(30, 15))

        # Messaggio
        ctk.CTkLabel(
            modal,
            text="Verrai mandato alla Home Page.",
            font=("Arial", 16),
            text_color="#ffffff",
        ).pack(pady=(5, 25))

        # Funzione di conferma
        def conferma():
            clear_token()  # <- Rimuove il token salvato
            modal.destroy()
            self.container.destroy()  # elimina tutta la MainView
            from app import HomePage

            HomePage(self.master)  # mostra la HomePage

        # Pulsanti
        buttons_frame = ctk.CTkFrame(modal, fg_color="transparent")
        buttons_frame.pack(pady=10)

        ctk.CTkButton(
            buttons_frame,
            text="✅ Conferma",
            command=conferma,
            width=180,
            height=50,
            fg_color="#e63946",
            hover_color="#ff4d5a",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, padx=15)

        ctk.CTkButton(
            buttons_frame,
            text="❌ Annulla",
            command=modal.destroy,
            width=180,
            height=50,
            fg_color="#888888",
            hover_color="#aaaaaa",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=1, padx=15)

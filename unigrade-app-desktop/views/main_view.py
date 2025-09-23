import customtkinter as ctk
from utils import set_app_icon


class MainView:
    def __init__(self, master, student_id):
        self.master = master
        self.student_id = student_id

        # --- Container principale della MainView ---
        self.container = ctk.CTkFrame(master)
        self.container.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self.container, width=200, corner_radius=0, fg_color="#11111b"
        )
        self.sidebar.pack(side="left", fill="y")

        # Content
        self.content = ctk.CTkFrame(
            self.container, corner_radius=20, fg_color="#2e2e3e"
        )
        self.content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        # Header frame per icona refresh (se vuoi usarlo nella content)
        self.header_frame = ctk.CTkFrame(
            self.content, fg_color="transparent", height=40
        )
        self.header_frame.pack(fill="x", pady=(0, 10))

        # Sidebar buttons
        buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📚 Libretto", self.show_libretto),
            ("🚪 Logout", self.logout),
        ]
        for text, cmd in buttons:
            ctk.CTkButton(self.sidebar, text=text, command=cmd, anchor="w").pack(
                fill="x", pady=5, padx=10
            )

        self.show_dashboard()

    def show_dashboard(self):
        from views.main_sub_view.dashboard_view import DashboardView

        for w in self.content.winfo_children():
            w.destroy()
        DashboardView(self.content, self.student_id)

    def show_libretto(self):
        from views.main_sub_view.libretto_view import LibrettoView

        for w in self.content.winfo_children():
            w.destroy()
        LibrettoView(self.content, self.student_id)

    def logout(self):
        import customtkinter as ctk
        from utils import set_app_icon  # icona finestra

        # Finestra modale
        modal = ctk.CTkToplevel(self.master)
        modal.title("Conferma Logout")
        modal.geometry("400x250")
        modal.grab_set()
        modal.resizable(False, False)
        set_app_icon(modal)

        # Titolo
        ctk.CTkLabel(
            modal,
            text="⚠️ Sei sicuro di voler uscire?",
            font=("Arial", 20, "bold"),
            text_color="#ff5555",
        ).pack(pady=(30, 10))

        # Messaggio
        ctk.CTkLabel(
            modal,
            text="Verrai mandato alla Home Page.",
            font=("Arial", 14),
            text_color="#ffffff",
        ).pack(pady=(5, 20))

        # Funzione di conferma
        def conferma():
            # clear_token()  # se vuoi mantenere le credenziali, lascia commentato
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
            width=150,
            fg_color="#e63946",
            hover_color="#ff4d5a",
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            buttons_frame,
            text="❌ Annulla",
            command=modal.destroy,
            width=150,
            fg_color="#888888",
            hover_color="#aaaaaa",
        ).grid(row=0, column=1, padx=10)

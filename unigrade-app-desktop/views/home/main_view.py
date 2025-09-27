import customtkinter as ctk
from configuration.unigrade_configuration import set_app_icon
from configuration.unigrade_token_configuration import clear_token

from views.home.home_view_components.home_sidebar_component import HomeSidebar
from views.home.home_view_components.home_header_component import HomeHeader
from views.home.home_view_components.home_content_component import HomeContent


class MainView:
    def __init__(self, master, student_id):
        self.master = master
        self.student_id = student_id

        # Container principale
        self.container = ctk.CTkFrame(master)
        self.container.pack(fill="both", expand=True)

        # Content components
        self.sidebar_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📚 Libretto", self.show_libretto),
            ("🚪 Logout", self.logout),
        ]
        self.sidebar = HomeSidebar(self.container, self.sidebar_buttons)
        self.content = HomeContent(self.container)
        self.header_frame = HomeHeader(self.content)

        # Mostra la dashboard di default
        self.show_dashboard()

    def show_dashboard(self):
        from views.home.home_view_components.dashboard.dashboard_view import (
            DashboardView,
        )

        self.content.clear()
        dashboard = DashboardView(self.content, self.student_id)
        dashboard.pack(fill="both", expand=True)

    def show_libretto(self):
        from views.home.home_view_components.libretto.libretto_view import LibrettoView

        self.content.clear()
        LibrettoView(self.content, self.student_id)

    def logout(self):
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

        def conferma():
            clear_token()
            modal.destroy()
            self.container.destroy()
            from app import HomePage

            HomePage(self.master)

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

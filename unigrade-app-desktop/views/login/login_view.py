import customtkinter as ctk

from configuration.unigrade_configuration import set_app_icon
from configuration.unigrade_token_configuration import load_token

from views.login.login_view_components.login_title_component import LoginTitle
from views.login.login_view_components.login_form_component import LoginForm
from views.login.login_view_components.login_checkbox_component import RememberCheckbox
from views.login.service.login_view_service import (
    LoginService,
)  # <--- il nostro nuovo service


class LoginView:
    def __init__(self, master, previous_view=None):
        self.master = master
        self.previous_view = previous_view

        # Imposta icona finestra
        set_app_icon(self.master)

        # Frame principale
        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.pack(expand=True, fill="both", padx=150, pady=150)

        # Service
        self.login_service = LoginService(frame=self.frame, master=self.master)

        # Titolo
        self.title = LoginTitle(self.frame)
        self.title.pack(pady=30)

        # Form
        self.form = LoginForm(self.frame)
        self.form.pack(pady=10)

        # Checkbox Remember Me
        self.remember_var = ctk.IntVar()
        self.checkbox = RememberCheckbox(self.frame, self.remember_var)
        self.checkbox.pack(pady=5)

        # Carica token se presente e tenta login automatico
        token_data = load_token()
        if token_data:
            student_id = self.login_service.auto_login()
            if student_id:
                # Inserisce matricola e seleziona checkbox
                self.form.entry_matricola.insert(
                    0, self.login_service.validate_token(token_data)["matricola"]
                )
                self.remember_var.set(1)
                self.master.after(500, lambda: self.open_main(student_id))

        # Bottoni integrati nel frame
        self.login_button = ctk.CTkButton(
            self.frame, text="Login", command=self.do_login, width=200
        )
        self.login_button.pack(pady=(15, 5))

        self.register_button = ctk.CTkButton(
            self.frame, text="Registrati", command=self.show_register, width=200
        )
        self.register_button.pack(pady=(5, 10))

        if self.previous_view:
            self.back_button = ctk.CTkButton(
                self.frame,
                text="Indietro",
                command=self.go_back,
                width=200,
                fg_color="#888888",
            )
            self.back_button.pack(pady=10)

    # ---------------- Login manuale ----------------
    def do_login(self):
        matricola = self.form.entry_matricola.get().strip()
        password = self.form.entry_password.get().strip()
        remember = self.remember_var.get() == 1

        student_id = self.login_service.do_login(matricola, password, remember)
        if student_id:
            self.master.after(1200, lambda: self.open_main(student_id))

    # ---------------- Navigazione ----------------
    def open_main(self, student_id):
        self.frame.destroy()
        from views.home.main_view import MainView

        MainView(self.master, student_id)

    def show_register(self):
        self.frame.destroy()
        from views.register.register_view import RegisterView

        RegisterView(
            self.master,
            previous_view=lambda: LoginView(
                self.master, previous_view=self.previous_view
            ),
        )

    def go_back(self):
        self.frame.destroy()
        if self.previous_view:
            self.previous_view()

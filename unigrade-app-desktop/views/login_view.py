import customtkinter as ctk
from controllers.auth_controller import login
from tkinter import messagebox

class LoginView:
    def __init__(self, master, previous_view=None):
        self.master = master
        self.previous_view = previous_view  # view precedente per il back button

        # Frame principale: espande per occupare tutta la finestra
        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.pack(expand=True, fill="both", padx=150, pady=150)  # maggiore padding

        # Titolo
        ctk.CTkLabel(self.frame, text="UniGrade", font=("Arial", 36, "bold")).pack(pady=30)

        # Entry
        self.entry_matr = ctk.CTkEntry(self.frame, placeholder_text="Matricola", width=300)
        self.entry_matr.pack(pady=15)
        self.entry_pw = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*", width=300)
        self.entry_pw.pack(pady=15)

        # Bottoni
        ctk.CTkButton(self.frame, text="Login", command=self.do_login, width=200).pack(pady=15)
        ctk.CTkButton(self.frame, text="Registrati", command=self.show_register, width=200).pack(pady=10)

        # Bottone Back
        if self.previous_view:
            ctk.CTkButton(self.frame, text="Indietro", command=self.go_back, width=200, fg_color="#888888").pack(pady=10)

    def do_login(self):
        matricola = self.entry_matr.get().strip()
        password = self.entry_pw.get().strip()

        # Controllo campi vuoti
        if not matricola or not password:
            messagebox.showerror("Errore", "Tutti i campi devono essere compilati!")
            return

        student_id = login(matricola, password)
        if student_id:
            self.frame.destroy()
            from views.main_view import MainView
            MainView(self.master, student_id)
        else:
            messagebox.showerror("Errore", "Credenziali errate!")

    def show_register(self):
        self.frame.destroy()
        from views.register_view import RegisterView
        RegisterView(self.master, previous_view=lambda: LoginView(self.master, previous_view=self.previous_view))

    def go_back(self):
        self.frame.destroy()
        if self.previous_view:
            self.previous_view()

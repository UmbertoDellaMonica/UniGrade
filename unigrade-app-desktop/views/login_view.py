import customtkinter as ctk

from controllers.auth_controller import login
from controllers.student_controller import get_student_by_matricola

from utils import show_temp_message, set_app_icon
from utils import save_token, load_token, clear_token, hash_password


import jwt
import datetime

# Chiave segreta locale per firmare i token JWT
JWT_SECRET = "unigrade_local_secret_key"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_DAYS = 7  # token valido 7 giorni


class LoginView:
    def __init__(self, master, previous_view=None):
        self.master = master
        self.previous_view = previous_view

        # Imposta l'icona della finestra principale
        set_app_icon(self.master)

        # Frame principale
        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.pack(expand=True, fill="both", padx=150, pady=150)

        # Titolo
        ctk.CTkLabel(self.frame, text="UniGrade", font=("Arial", 36, "bold")).pack(
            pady=30
        )

        # Entry matricola e password
        self.entry_matr = ctk.CTkEntry(
            self.frame, placeholder_text="Matricola", width=300
        )
        self.entry_matr.pack(pady=15)
        self.entry_pw = ctk.CTkEntry(
            self.frame, placeholder_text="Password", show="*", width=300
        )
        self.entry_pw.pack(pady=15)

        # Checkbox Remember Me
        self.remember_var = ctk.IntVar()
        ctk.CTkCheckBox(self.frame, text="Ricordami", variable=self.remember_var).pack(
            pady=5
        )

        # Carica token se presente e prova login automatico
        token_data = load_token()
        if token_data:
            decoded = self.validate_token(token_data)
            if decoded:
                matricola = decoded.get("matricola")
                self.entry_matr.insert(0, matricola)
                self.remember_var.set(1)
                # Login automatico con piccolo delay
                self.master.after(500, lambda: self.auto_login())

        # Bottoni
        ctk.CTkButton(self.frame, text="Login", command=self.do_login, width=200).pack(
            pady=15
        )
        ctk.CTkButton(
            self.frame, text="Registrati", command=self.show_register, width=200
        ).pack(pady=10)

        # Bottone Back
        if self.previous_view:
            ctk.CTkButton(
                self.frame,
                text="Indietro",
                command=self.go_back,
                width=200,
                fg_color="#888888",
            ).pack(pady=10)

    def generate_token(self, matricola, passowrd_hashed):
        """Genera un token JWT firmato con la matricola e data di scadenza"""
        exp = datetime.datetime.utcnow() + datetime.timedelta(days=JWT_EXP_DELTA_DAYS)
        payload = {
            "matricola": matricola,
            "pw_hash": passowrd_hashed,
            "exp": exp.timestamp(),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    def validate_token(self, token):
        """Decodifica e valida il token JWT, ritorna payload se valido, None altrimenti"""
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            clear_token()
            return None

    # Check students credentials with the logic of JWT token
    def login_with_hash(self, matricola, pw_hash):

        print("Credenziali passate : ")
        print(matricola)
        print(pw_hash)
        # Fetch Student from Database
        student = get_student_by_matricola(matricola)  # recupera utente dal DB
        print(f"Studente ottenuto : {student}")
        if student and student["password"] == pw_hash:
            print(" Studente con ID :")
            return student["id"]

        return None

    def auto_login(self):
        """Login automatico decodificando il token e validando con database"""
        token_data = load_token()
        if not token_data:
            return

        decoded = self.validate_token(token_data)
        if not decoded:
            return

        matricola = decoded["matricola"]
        pw_hash = decoded["pw_hash"]

        print(f"Matricola from Token : {matricola}")
        print(f"Password Hashed from Token : {pw_hash}")

        # Check students with Hash Password on Database
        print("Sto per effettuare il check del Password Hashata ")
        student_id = self.login_with_hash(matricola, pw_hash)

        if student_id:
            show_temp_message(
                self.frame, "✅ Login automatico effettuato!", color="green"
            )
            self.master.after(1200, lambda: self.open_main(student_id))
        else:
            clear_token()
            show_temp_message(
                self.frame,
                "⚠️ Token scaduto o invalido, inserisci le credenziali!",
                color="red",
            )

    def do_login(self):
        matricola = self.entry_matr.get().strip()
        password = self.entry_pw.get().strip()

        if not matricola or not password:
            show_temp_message(
                self.frame, "⚠️ Tutti i campi devono essere compilati!", color="red"
            )
            return

            # Do Login and retrieve Student ID
        student_id = login(matricola, password)

        if student_id:
            # Salva token se Remember Me è selezionato
            if self.remember_var.get():
                # Generate Token for the next session
                token = self.generate_token(
                    matricola, passowrd_hashed=hash_password(password)
                )
                # Save token session
                save_token(token)
            else:
                # Delete token
                clear_token()

            show_temp_message(
                self.frame, "✅ Login effettuato con successo!", color="green"
            )
            self.master.after(1200, lambda: self.open_main(student_id))

        else:
            show_temp_message(self.frame, "❌ Credenziali errate!", color="red")

    def open_main(self, student_id):
        self.frame.destroy()
        from views.main_view import MainView

        MainView(self.master, student_id)

    def show_register(self):
        self.frame.destroy()
        from views.register_view import RegisterView

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

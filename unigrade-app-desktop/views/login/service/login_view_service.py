# services/login_service.py
import datetime
import jwt
from controllers.auth_controller import login
from controllers.student_controller import get_student_by_matricola
from configuration.unigrade_configuration import (
    JWT_ALGORITHM,
    JWT_EXP_DELTA_DAYS,
    JWT_SECRET,
)
from configuration.unigrade_token_configuration import (
    save_token,
    load_token,
    clear_token,
)
from configuration.database_configuration import hash_password
from configuration.unigrade_configuration import show_temp_message


class LoginService:
    def __init__(self, frame=None, master=None):
        """
        frame: opzionale, usato per mostrare messaggi toast con show_temp_message
        master: opzionale, usato per after() per login automatico
        """
        self.frame = frame
        self.master = master

    # ---------------- Token & JWT ----------------
    def generate_token(self, matricola, password_hashed):
        exp = datetime.datetime.utcnow() + datetime.timedelta(days=JWT_EXP_DELTA_DAYS)
        payload = {
            "matricola": matricola,
            "pw_hash": password_hashed,
            "exp": exp.timestamp(),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    def validate_token(self, token):
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            clear_token()
            return None

    # ---------------- Login con hash ----------------
    def login_with_hash(self, matricola, pw_hash):
        student = get_student_by_matricola(matricola)
        if student and student["password"] == pw_hash:
            return student["id"]
        return None

    # ---------------- Login automatico ----------------
    def auto_login(self):
        token_data = load_token()
        if not token_data:
            return None

        decoded = self.validate_token(token_data)
        if not decoded:
            return None

        student_id = self.login_with_hash(decoded["matricola"], decoded["pw_hash"])
        if student_id:
            if self.frame:
                show_temp_message(
                    self.frame, "✅ Login automatico effettuato!", color="green"
                )
            return student_id
        else:
            clear_token()
            if self.frame:
                show_temp_message(
                    self.frame,
                    "⚠️ Token scaduto o invalido, inserisci le credenziali!",
                    color="red",
                )
            return None

    # ---------------- Login manuale ----------------
    def do_login(self, matricola: str, password: str, remember: bool):
        if not matricola or not password:
            if self.frame:
                show_temp_message(
                    self.frame, "⚠️ Tutti i campi devono essere compilati!", color="red"
                )
            return None

        student_id = login(matricola, password)
        if student_id:
            if remember:
                token = self.generate_token(matricola, hash_password(password))
                save_token(token)
            else:
                clear_token()

            if self.frame:
                show_temp_message(
                    self.frame, "✅ Login effettuato con successo!", color="green"
                )
            return student_id
        else:
            if self.frame:
                show_temp_message(self.frame, "❌ Credenziali errate!", color="red")
            return None

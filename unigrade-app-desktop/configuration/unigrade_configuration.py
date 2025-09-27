import os, sys
import customtkinter as ctk

from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()


# --- DB ---
DB_NAME = os.getenv("DB_NAME", "unigrade.db")

# --- APP ---
APP_NAME = os.getenv("APP_NAME", "UniGrade")

# --- JWT ---
JWT_SECRET = os.getenv("JWT_SECRET", "unigrade_local_secret_key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_DELTA_DAYS = int(os.getenv("JWT_EXP_DELTA_DAYS", 7))


# ---- Service ----


def resource_path(relative_path):
    """Ritorna il path assoluto di un file, anche dentro il bundle PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Icon Logo
def set_app_icon(window):
    """Imposta l'icona per una finestra Tk/CTk"""
    icon_path = resource_path("assets/unigrade-logo-icon.ico")  # usa resource_path
    try:
        window.iconbitmap(icon_path)
    except Exception as e:
        print(f"[WARN] Impossibile impostare l'icona: {e}")


def show_temp_message(parent, text, color="green", duration=2000):
    """
    Mostra un messaggio temporaneo centrato in alto che scompare automaticamente.

    Args:
        parent: il widget padre (di solito un frame o la root)
        text: testo del messaggio
        color: colore sfondo (es. "green", "red", "#ffaa00")
        duration: tempo in ms prima che scompaia (default 2000ms = 2s)
    """
    msg = ctk.CTkLabel(
        parent,
        text=text,
        fg_color=color,
        text_color="white",
        corner_radius=10,
        padx=10,
        pady=5,
    )
    # Appare sempre in alto, centrato orizzontalmente
    msg.place(relx=0.5, rely=0.02, anchor="n")  # più vicino al bordo superiore

    # dopo `duration` millisecondi distrugge il messaggio
    parent.after(duration, msg.destroy)

import hashlib
import os
import customtkinter as ctk
import json
import os


# Hash Password - UniGrade Application
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Icon Logo 
def set_app_icon(window):
    """Imposta l'icona per una finestra Tk/CTk"""
    icon_path = os.path.join("assets", "unigrade-logo-icon.ico")
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
        parent, text=text, fg_color=color, text_color="white",
        corner_radius=10, padx=10, pady=5
    )
    # Appare sempre in alto, centrato orizzontalmente
    msg.place(relx=0.5, rely=0.02, anchor="n")  # più vicino al bordo superiore

    # dopo `duration` millisecondi distrugge il messaggio
    parent.after(duration, msg.destroy)

##################### TOKEN - Service #####################

TOKEN_FILE = "session.token"

def save_token(token: str):
    """Salva il token JWT su file locale"""
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

def load_token() -> str | None:
    """Carica il token JWT dal file, se presente"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

def clear_token():
    """Rimuove il file del token JWT"""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)

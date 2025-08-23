import hashlib
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





import customtkinter as ctk

def show_temp_message(parent, text, color="green", duration=2000):
    """
    Mostra un messaggio temporaneo che scompare automaticamente.
    
    Args:
        parent: il widget padre (di solito un frame o la root)
        text: testo del messaggio
        color: colore sfondo (es. "green", "red", "#ffaa00")
        duration: tempo in ms prima che scompaia (default 2000ms = 2s)
    """
    msg = ctk.CTkLabel(parent, text=text, fg_color=color, text_color="white", corner_radius=10, padx=10, pady=5)
    msg.place(relx=0.5, rely=0.05, anchor="n")  # appare in alto, centrato

    # dopo `duration` millisecondi distrugge il messaggio
    parent.after(duration, msg.destroy)

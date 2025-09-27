import os

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

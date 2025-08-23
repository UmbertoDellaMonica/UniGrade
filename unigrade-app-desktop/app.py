import customtkinter as ctk
from database import init_db
from views.login_view import LoginView

if __name__ == "__main__":
    init_db()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    # Adatta alle dimensioni dello schermo
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Opzionale: lascia un piccolo margine di 50 px su ciascun lato
    width = screen_width - 100
    height = screen_height - 100

    root.geometry(f"{width}x{height}+50+50")
    root.title("UniGrade - Libretto Universitario Digitale")

    LoginView(root)
    root.mainloop()

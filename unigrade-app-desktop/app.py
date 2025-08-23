import customtkinter as ctk
from database import init_db
from views.login_view import LoginView
from utils import set_app_icon

if __name__ == "__main__":
    init_db()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    # adatta alle dimensioni dello schermo
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width - 100
    height = screen_height - 100
    root.geometry(f"{width}x{height}+50+50")

    root.title("UniGrade - Libretto Universitario Digitale")
    set_app_icon(root)  # 👈 icona qui

    LoginView(root)
    root.mainloop()

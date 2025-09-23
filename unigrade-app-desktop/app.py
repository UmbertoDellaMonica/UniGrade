import customtkinter as ctk
from configuration.database_configuration import init_db
from views.login_view import LoginView
from views.register_view import RegisterView
from utils import set_app_icon


class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.master = master

        master.title("UniGrade - Libretto Universitario Digitale")
        set_app_icon(master)

        # --- Sfondo principale ---
        self.bg_frame = ctk.CTkFrame(self, fg_color="#1c1c1c", corner_radius=0)
        self.bg_frame.pack(fill="both", expand=True)

        # --- Frame centrale per centrare il contenuto ---
        self.center_frame = ctk.CTkFrame(self.bg_frame, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")  # centro esatto

        # --- Logo / titolo stilizzato ---
        self.title_label = ctk.CTkLabel(
            self.center_frame,
            text="UniGrade",
            font=("Arial", 48, "bold"),
            text_color="#4da6ff",
        )
        self.title_label.pack(pady=(0, 20))

        # --- Slogan ---
        self.subtitle_label = ctk.CTkLabel(
            self.center_frame,
            text="La tua università a portata di click",
            font=("Arial", 18, "italic"),
            text_color="#aaaaaa",
        )
        self.subtitle_label.pack(pady=(0, 40))

        # --- Pulsanti centrali ---
        self.button_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.button_frame.pack()

        # Login
        self.login_btn = ctk.CTkButton(
            self.button_frame,
            text="🔑 Login",
            font=("Arial", 16, "bold"),
            width=200,
            height=50,
            corner_radius=25,
            fg_color="#4da6ff",
            hover_color="#66b3ff",
            command=self.go_to_login,
        )
        self.login_btn.grid(row=0, column=0, padx=20, pady=10)

        # Registrati
        self.register_btn = ctk.CTkButton(
            self.button_frame,
            text="📝 Registrati",
            font=("Arial", 16, "bold"),
            width=200,
            height=50,
            corner_radius=25,
            fg_color="#2a2a2a",
            hover_color="#444",
            command=self.go_to_register,
        )
        self.register_btn.grid(row=0, column=1, padx=20, pady=10)

    # Navigazione
    def go_to_login(self):
        self.destroy()
        LoginView(self.master)

    def go_to_register(self):
        self.destroy()
        RegisterView(self.master)


if __name__ == "__main__":
    init_db()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    # Ottieni le dimensioni dello schermo
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Imposta la finestra alla dimensione massima dello schermo
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.minsize(800, 600)  # facoltativo: dimensione minima

    # Rimuovi margini interni
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Avvia HomePage
    homepage = HomePage(root)
    homepage.grid(row=0, column=0, sticky="nsew")

    root.mainloop()

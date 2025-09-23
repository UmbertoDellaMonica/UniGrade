import customtkinter as ctk
from controllers.auth_controller import register
from views.login_view import LoginView
from utils import show_temp_message  # import della funzione toast


class RegisterView:
    def __init__(self, master, previous_view=None):
        self.master = master
        self.previous_view = previous_view

        # Frame principale
        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Titolo
        ctk.CTkLabel(
            self.frame, text="Crea il tuo account", font=("Arial", 24, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(20, 40))

        # Campi base (tranne Corso)
        self.entries = {}
        self.labels = ["Nome", "Cognome", "Matricola", "Password"]

        for i, lbl in enumerate(self.labels):
            ctk.CTkLabel(self.frame, text=lbl, font=("Arial", 14)).grid(
                row=i + 1, column=0, sticky="e", padx=(20, 10), pady=10
            )
            ent = ctk.CTkEntry(
                self.frame, show="*" if "Password" in lbl else None, width=250
            )
            ent.grid(row=i + 1, column=1, sticky="w", padx=(10, 20), pady=10)
            self.entries[lbl] = ent

        # Selezione Corso (dropdown)
        ctk.CTkLabel(self.frame, text="Corso di Laurea", font=("Arial", 14)).grid(
            row=len(self.labels) + 1, column=0, sticky="e", padx=(20, 10), pady=10
        )
        self.course_var = ctk.StringVar(value="Triennale")  # default
        course_dropdown = ctk.CTkOptionMenu(
            self.frame,
            values=["Triennale", "Magistrale"],
            variable=self.course_var,
            width=250,
        )
        course_dropdown.grid(
            row=len(self.labels) + 1, column=1, sticky="w", padx=(10, 20), pady=10
        )

        # Entry per Facoltà
        ctk.CTkLabel(self.frame, text="Facoltà", font=("Arial", 14)).grid(
            row=len(self.labels) + 2, column=0, sticky="e", padx=(20, 10), pady=10
        )
        self.entries["Facoltà"] = ctk.CTkEntry(self.frame, width=250)
        self.entries["Facoltà"].grid(
            row=len(self.labels) + 2, column=1, sticky="w", padx=(10, 20), pady=10
        )

        # Bottone conferma
        ctk.CTkButton(
            self.frame, text="Conferma", command=self.do_register, width=200
        ).grid(row=len(self.labels) + 3, column=0, columnspan=2, pady=(30, 10))

        # Bottone Back
        ctk.CTkButton(
            self.frame,
            text="Indietro",
            command=self.go_back,
            width=200,
            fg_color="#888888",
        ).grid(row=len(self.labels) + 4, column=0, columnspan=2, pady=(5, 20))

    def do_register(self):
        # Validazione campi
        for lbl, widget in self.entries.items():
            if not widget.get().strip():
                show_temp_message(
                    self.frame, f"⚠️ Il campo '{lbl}' non può essere vuoto!", color="red"
                )
                return

        # Tentativo registrazione
        success = register(
            self.entries["Nome"].get().strip(),
            self.entries["Cognome"].get().strip(),
            self.course_var.get().strip() + " " + self.entries["Facoltà"].get().strip(),
            self.entries["Matricola"].get().strip(),
            self.entries["Password"].get().strip(),
        )

        if success:
            show_temp_message(
                self.frame, "✅ Registrazione completata con successo!", color="green"
            )
            self.master.after(1500, self.go_back)  # torna indietro dopo 1.5s
        else:
            show_temp_message(self.frame, "❌ Matricola già registrata!", color="red")

    def go_back(self):
        self.frame.destroy()
        if self.previous_view:
            self.previous_view()
        else:
            from app import HomePage  # import locale, evita circular import

            HomePage(self.master)

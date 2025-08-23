import customtkinter as ctk
from tkinter import messagebox
from controllers.auth_controller import register
from views.login_view import LoginView  # import locale se vuoi evitare circolarità

class RegisterView:
    def __init__(self, master, previous_view=None):
        self.master = master
        self.previous_view = previous_view  # memorizza la view precedente

        # Frame principale
        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Titolo
        ctk.CTkLabel(self.frame, text="Crea il tuo account", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=(20,40))

        # Campi
        self.entries = {}
        self.labels = ["Nome", "Cognome", "Corso (Triennale/Magistrale)", "Matricola", "Password"]
        for i, lbl in enumerate(self.labels):
            ctk.CTkLabel(self.frame, text=lbl, font=("Arial", 14)).grid(row=i+1, column=0, sticky="e", padx=(20,10), pady=10)
            ent = ctk.CTkEntry(self.frame, show="*" if "Password" in lbl else None, width=250)
            ent.grid(row=i+1, column=1, sticky="w", padx=(10,20), pady=10)
            self.entries[lbl] = ent

        # Bottone conferma
        ctk.CTkButton(self.frame, text="Conferma", command=self.do_register, width=200).grid(row=len(self.labels)+1, column=0, columnspan=2, pady=(30,10))

        # Bottone Back
        ctk.CTkButton(self.frame, text="Indietro", command=self.go_back, width=200, fg_color="#888888").grid(row=len(self.labels)+2, column=0, columnspan=2, pady=(5,20))

    def do_register(self):
        for lbl in self.labels:
            if not self.entries[lbl].get().strip():
                messagebox.showerror("Errore", f"Il campo '{lbl}' non può essere vuoto!")
                return

        success = register(
            self.entries["Nome"].get().strip(),
            self.entries["Cognome"].get().strip(),
            self.entries["Corso (Triennale/Magistrale)"].get().strip(),
            self.entries["Matricola"].get().strip(),
            self.entries["Password"].get().strip()
        )

        if success:
            messagebox.showinfo("OK", "Registrazione completata!")
            self.frame.destroy()
            if self.previous_view:
                self.previous_view()  # torna alla view precedente
            else:
                LoginView(self.master)
        else:
            messagebox.showerror("Errore", "Matricola già registrata!")

    def go_back(self):
        self.frame.destroy()
        if self.previous_view:
            self.previous_view()
        else:
            LoginView(self.master)

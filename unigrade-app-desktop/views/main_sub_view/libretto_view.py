

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from controllers.exam_controller import get_exams, add_exam, update_exam, remove_exam
from utils import resource_path, set_app_icon

class LibrettoView(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.student_id = student_id

        # Header principale
        ctk.CTkLabel(
            self, 
            text="📚 Libretto Esami", 
            font=("Arial", 24, "bold")
        ).pack(pady=(10,20))

        # Frame principale
        libretto_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#2e2e3e")
        libretto_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Icone per intestazioni ---
        self.icons = {
            "exam": ImageTk.PhotoImage(Image.open(resource_path("assets/icons/book.png")).resize((20,20))),
            "vote": ImageTk.PhotoImage(Image.open(resource_path("assets/icons/star.png")).resize((20,20))),
            "cfu": ImageTk.PhotoImage(Image.open(resource_path("assets/icons/coin.png")).resize((20,20))),
            "status": ImageTk.PhotoImage(Image.open(resource_path("assets/icons/check.png")).resize((20,20))),
        }

        headers = [
            ("Nome Esame", self.icons["exam"]),
            ("Voto", self.icons["vote"]),
            ("CFU", self.icons["cfu"]),
            ("Stato", self.icons["status"]),
        ]

        # --- Header personalizzato ---
        header_frame = ctk.CTkFrame(libretto_frame, fg_color="#2b2b3d", corner_radius=8)
        header_frame.pack(fill="x", pady=(5,0))

        for text, icon in headers:
            lbl = ctk.CTkLabel(
                header_frame,
                text=f" {text}",
                image=icon,
                compound="left",
                font=("Arial", 14, "bold"),
                padx=10
            )
            lbl.pack(side="left", expand=True, fill="x", padx=5, pady=5)

        # --- Treeview ---
        cols = ("Nome Esame", "Voto", "CFU", "Stato")
        self.tree = ttk.Treeview(
            libretto_frame,
            columns=cols,
            show="headings",
            height=14
        )

        # Stile tabella
        style = ttk.Style()
        style.configure("Treeview",
            background="#1e1e2f",
            foreground="white",
            rowheight=40,
            fieldbackground="#1e1e2f",
            font=("Arial", 13)
        )
        style.map("Treeview", background=[("selected", "#4da6ff")])

        for col in cols:
            self.tree.column(col, anchor="center", width=200)

        self.tree.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Label media ponderata
        self.avg_label = ctk.CTkLabel(self, text="", font=("Arial", 15, "bold"))
        self.avg_label.pack(pady=(10,0))

        # Carica dati esami
        self.load_exams()

        # --- Bottoni ---
        btn_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#222233")
        btn_frame.pack(pady=15, padx=20, fill="x")

        ctk.CTkButton(btn_frame, text="➕ Aggiungi", command=self.add_exam,
                    width=150, fg_color="#4da6ff", hover_color="#66b3ff").pack(side="left", padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="✏️ Modifica", command=self.edit_exam,
                    width=150, fg_color="#ffb84d", hover_color="#ffc966").pack(side="left", padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="🗑️ Rimuovi", command=self.remove_exam,
                    width=150, fg_color="#ff4d4d", hover_color="#ff6666").pack(side="left", padx=10, pady=5)

    # --- Metodi di gestione esami ---
    def load_exams(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        exams = get_exams(self.student_id)
        total_weighted = 0
        total_cfu = 0
        for e in exams:
            stato = "Passato ✅" if e[2] >= 18 else "Non superato ❌"
            self.tree.insert("", "end", iid=e[0], values=(e[1], e[2], e[3], stato))
            total_weighted += e[2] * e[3]
            total_cfu += e[3]

        self.total_weighted = total_weighted
        self.total_cfu = total_cfu
        self.update_avg()

    def update_avg(self):
        if hasattr(self, 'total_cfu') and self.total_cfu > 0:
            media = self.total_weighted / self.total_cfu
            self.avg_label.configure(text=f"📊 Media ponderata: {media:.2f}")
        else:
            self.avg_label.configure(text="📊 Media ponderata: N/A")


    def add_exam(self):
        import customtkinter as ctk
        from tkinter import messagebox

        # Creiamo una finestra modale
        modal = ctk.CTkToplevel(self.master)
        modal.title("Aggiungi Nuovo Esame")
        modal.geometry("400x500")
        modal.grab_set()  # Blocca l'interazione con la finestra principale
        modal.resizable(False, False)
        set_app_icon(modal)


        # Titolo
        ctk.CTkLabel(modal, text="📚 Nuovo Esame", font=("Arial", 20, "bold")).pack(pady=(20,15))

        # Frame dei campi
        fields_frame = ctk.CTkFrame(modal, corner_radius=15, fg_color="#2e2e3e")
        fields_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Entry + Label per Nome
        ctk.CTkLabel(fields_frame, text="Nome Esame", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        entry_nome = ctk.CTkEntry(fields_frame, width=200)
        entry_nome.grid(row=0, column=1, padx=10, pady=10)

        # Entry + Label per Voto
        ctk.CTkLabel(fields_frame, text="Voto", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        entry_voto = ctk.CTkEntry(fields_frame, width=100)
        entry_voto.grid(row=1, column=1, padx=10, pady=10)

        # Entry + Label per CFU
        ctk.CTkLabel(fields_frame, text="CFU", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        entry_cfu = ctk.CTkEntry(fields_frame, width=100)
        entry_cfu.grid(row=2, column=1, padx=10, pady=10)

        # Label messaggi in tempo reale
        msg_label = ctk.CTkLabel(modal, text="", font=("Arial", 12), text_color="#ff6666")
        msg_label.pack(pady=(5,0))

        # Funzione di conferma
        def conferma():
            nome = entry_nome.get().strip()
            try:
                voto = int(entry_voto.get())
                cfu = int(entry_cfu.get())
            except ValueError:
                msg_label.configure(text="Voto e CFU devono essere numeri!")
                return

            if not nome or voto < 18 or voto > 30 or cfu <= 0:
                msg_label.configure(text="Controlla i valori inseriti!")
                return

            add_exam(self.student_id, nome, voto, cfu)
            self.load_exams()
            modal.destroy()
            # Breve messaggio di successo
            success = ctk.CTkLabel(self.master, text="✅ Esame aggiunto!", font=("Arial", 14, "bold"), text_color="#4dd17f")
            success.place(relx=0.5, rely=0.95, anchor="s")
            self.master.after(2000, success.destroy)

        # Pulsante conferma
        ctk.CTkButton(modal, text="Aggiungi", command=conferma, width=180, fg_color="#4da6ff", hover_color="#66b3ff").pack(pady=(20,15))

        # Pulsante annulla
        ctk.CTkButton(modal, text="Annulla", command=modal.destroy, width=180, fg_color="#888888", hover_color="#aaaaaa").pack(pady=(0,15))


    def edit_exam(self):
        import customtkinter as ctk
        from tkinter import messagebox

        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Attenzione", "Seleziona un esame da modificare!")
            return

        eid = sel[0]
        vals = self.tree.item(eid, "values")

        # Finestra modale
        modal = ctk.CTkToplevel(self.master)
        modal.title("Modifica Esame")
        modal.geometry("400x500")
        modal.grab_set()
        modal.resizable(False, False)
        set_app_icon(modal)


        # Titolo
        ctk.CTkLabel(modal, text="✏️ Modifica Esame", font=("Arial", 20, "bold")).pack(pady=(20,15))

        # Frame campi
        fields_frame = ctk.CTkFrame(modal, corner_radius=15, fg_color="#2e2e3e")
        fields_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Nome Esame
        ctk.CTkLabel(fields_frame, text="Nome Esame", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        entry_nome = ctk.CTkEntry(fields_frame, width=200)
        entry_nome.insert(0, vals[0])  # Precompila
        entry_nome.grid(row=0, column=1, padx=10, pady=10)

        # Voto
        ctk.CTkLabel(fields_frame, text="Voto", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        entry_voto = ctk.CTkEntry(fields_frame, width=100)
        entry_voto.insert(0, vals[1])
        entry_voto.grid(row=1, column=1, padx=10, pady=10)

        # CFU
        ctk.CTkLabel(fields_frame, text="CFU", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        entry_cfu = ctk.CTkEntry(fields_frame, width=100)
        entry_cfu.insert(0, vals[2])
        entry_cfu.grid(row=2, column=1, padx=10, pady=10)

        # Label messaggi
        msg_label = ctk.CTkLabel(modal, text="", font=("Arial", 12), text_color="#ff6666")
        msg_label.pack(pady=(5,0))

        # Funzione conferma
        def conferma():
            nome = entry_nome.get().strip()
            try:
                voto = int(entry_voto.get())
                cfu = int(entry_cfu.get())
            except ValueError:
                msg_label.configure(text="Voto e CFU devono essere numeri!")
                return

            if not nome or voto < 18 or voto > 30 or cfu <= 0:
                msg_label.configure(text="Controlla i valori inseriti!")
                return

            update_exam(eid, nome, voto, cfu)
            self.load_exams()
            modal.destroy()

            # Messaggio di successo
            success = ctk.CTkLabel(self.master, text="✅ Esame modificato!", font=("Arial", 14, "bold"), text_color="#4dd17f")
            success.place(relx=0.5, rely=0.95, anchor="s")
            self.master.after(2000, success.destroy)

        # Pulsanti
        ctk.CTkButton(modal, text="Salva Modifiche", command=conferma,
                    width=180, fg_color="#4da6ff", hover_color="#66b3ff").pack(pady=(20,15))
        ctk.CTkButton(modal, text="Annulla", command=modal.destroy,
                    width=180, fg_color="#888888", hover_color="#aaaaaa").pack(pady=(0,15))


    def remove_exam(self):
        import customtkinter as ctk
        from tkinter import messagebox

        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Attenzione", "Seleziona un esame da eliminare!")
            return

        eid = sel[0]
        vals = self.tree.item(eid, "values")

        # Finestra modale
        modal = ctk.CTkToplevel(self.master)
        modal.title("Conferma Eliminazione")
        modal.geometry("400x250")
        modal.grab_set()
        modal.resizable(False, False)
        set_app_icon(modal)


        # Titolo
        ctk.CTkLabel(modal, text="⚠️ Eliminare Esame?", font=("Arial", 20, "bold"), text_color="#ff5555").pack(pady=(20, 10))

        # Messaggio con info esame
        info_text = f"Nome: {vals[0]}\nVoto: {vals[1]}\nCFU: {vals[2]}"
        ctk.CTkLabel(modal, text=info_text, font=("Arial", 14), text_color="#ffffff").pack(pady=(5, 20))

        # Funzione di conferma
        def conferma():
            remove_exam(eid)
            self.load_exams()
            modal.destroy()
            # Messaggio successo
            success = ctk.CTkLabel(self.master, text="🗑️ Esame eliminato!", font=("Arial", 14, "bold"), text_color="#ff6666")
            success.place(relx=0.5, rely=0.95, anchor="s")
            self.master.after(2000, success.destroy)

        # Pulsanti
        buttons_frame = ctk.CTkFrame(modal, fg_color="transparent")
        buttons_frame.pack(pady=10)

        ctk.CTkButton(buttons_frame, text="✅ Conferma", command=conferma,
                    width=150, fg_color="#e63946", hover_color="#ff4d5a").grid(row=0, column=0, padx=10)

        ctk.CTkButton(buttons_frame, text="❌ Annulla", command=modal.destroy,
                    width=150, fg_color="#888888", hover_color="#aaaaaa").grid(row=0, column=1, padx=10)
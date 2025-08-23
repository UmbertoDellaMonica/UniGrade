import customtkinter as ctk
from tkinter import ttk, simpledialog, messagebox
from controllers.exam_controller import get_exams, add_exam, update_exam, remove_exam

import matplotlib.pyplot as plt

class MainView:
    def __init__(self, master, student_id):
        self.master = master
        self.student_id = student_id

        # Sidebar
        self.sidebar = ctk.CTkFrame(master, width=200, corner_radius=0, fg_color="#11111b")
        self.sidebar.pack(side="left", fill="y")
        self.content = ctk.CTkFrame(master, corner_radius=20, fg_color="#2e2e3e")
        self.content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📚 Libretto", self.show_libretto),
            ("📈 Andamento", self.show_graph),
            ("🚪 Logout", self.logout)
        ]
        for text, cmd in buttons:
            ctk.CTkButton(self.sidebar, text=text, command=cmd, anchor="w").pack(fill="x", pady=5, padx=10)

        self.show_dashboard()

    def show_dashboard(self):
        for w in self.content.winfo_children(): w.destroy()
        ctk.CTkLabel(self.content, text="Benvenuto in UniGrade!", font=("Arial", 22, "bold")).pack(pady=20)
        ctk.CTkLabel(self.content, text="Usa la sidebar per navigare.", font=("Arial", 14)).pack(pady=10)

    def show_libretto(self):
        # Pulisci il content
        for w in self.content.winfo_children():
            w.destroy()

        # Header Libretto
        ctk.CTkLabel(
            self.content, 
            text="📚 Libretto Esami", 
            font=("Arial", 22, "bold")
        ).pack(pady=(10,20))

        # Frame principale dei dati
        libretto_frame = ctk.CTkFrame(self.content, corner_radius=15, fg_color="#2e2e3e")
        libretto_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview esami
        cols = ("Nome Esame", "Voto", "CFU", "Stato")
        self.tree = ttk.Treeview(libretto_frame, columns=cols, show="headings", height=12)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # **Creiamo prima la label della media ponderata**
        self.avg_label = ctk.CTkLabel(self.content, text="", font=("Arial", 14, "bold"))
        self.avg_label.pack(pady=(10,0))

        # Ora possiamo caricare gli esami e aggiornare la media
        self.load_exams()  

        # Frame bottoni gestione
        btn_frame = ctk.CTkFrame(self.content, corner_radius=10, fg_color="#222233")
        btn_frame.pack(pady=15, padx=20, fill="x")

        ctk.CTkButton(btn_frame, text="➕ Aggiungi", command=self.add_exam, width=150, fg_color="#4da6ff", hover_color="#66b3ff").pack(side="left", padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="✏️ Modifica", command=self.edit_exam, width=150, fg_color="#ffb84d", hover_color="#ffc966").pack(side="left", padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="🗑️ Rimuovi", command=self.remove_exam, width=150, fg_color="#ff4d4d", hover_color="#ff6666").pack(side="left", padx=10, pady=5)



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
        sel = self.tree.selection()
        if not sel: return
        eid = sel[0]
        vals = self.tree.item(eid, "values")
        new_nome = simpledialog.askstring("Modifica Esame","Nome:",initialvalue=vals[0])
        new_voto = simpledialog.askinteger("Modifica Voto","Voto:",initialvalue=int(vals[1]))
        new_cfu = simpledialog.askinteger("Modifica CFU","CFU:",initialvalue=int(vals[2]))
        if new_nome and new_voto and new_cfu:
            update_exam(eid, new_nome, new_voto, new_cfu)
            self.load_exams()

    def remove_exam(self):
        sel = self.tree.selection()
        if not sel: return
        remove_exam(sel[0])
        self.load_exams()

    def show_graph(self):
        exams = get_exams(self.student_id)
        voti = [e[2] for e in exams]
        if not voti:
            messagebox.showinfo("Info", "Nessun esame inserito!")
            return
        plt.style.use("seaborn-v0_8-darkgrid")
        plt.plot(range(1,len(voti)+1), voti, marker="o")
        plt.title("Andamento voti")
        plt.xlabel("Esami")
        plt.ylabel("Voto")
        plt.ylim(18,31)
        plt.show()

    def logout(self):
        # Distrugge i frame attuali e torna al login
        self.sidebar.destroy()
        self.content.destroy()
        from views.login_view import LoginView
        LoginView(self.master)

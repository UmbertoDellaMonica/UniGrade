import customtkinter as ctk
from tkinter import ttk, simpledialog, messagebox
from controllers.exam_controller import get_exams, add_exam, update_exam, remove_exam
from utils import set_app_icon
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

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
        # Distrugge i widget precedenti
        for w in self.content.winfo_children(): 
            w.destroy()

        # --- Scrollable Frame principale ---
        canvas = tk.Canvas(self.content, bg="#1c1c1c", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self.content, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Colonna sinistra: Avatar ---
        avatar_frame = ctk.CTkFrame(scrollable_frame, width=200, corner_radius=15)
        avatar_frame.pack(side="left", padx=20, pady=20, fill="y")
        self.avatar_label = ctk.CTkLabel(avatar_frame, text="Avatar", font=("Arial", 18))
        self.avatar_label.pack(pady=20)
        self.avatar_img_label = ctk.CTkLabel(avatar_frame, text="(clicca per caricare foto)", width=150, height=150, fg_color="#444")
        self.avatar_img_label.pack(pady=10)
        # TODO: aggiungere caricamento immagine al click

        # --- Card Info Utente ---
        info_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15, fg_color="#2a2a2a")
        info_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # Qui dovresti recuperare i dati reali dello studente dal DB
        nome, cognome, matricola, corso = "Mario", "Rossi", "123456", "Informatica"

        ctk.CTkLabel(info_frame, text=f"{nome} {cognome}", font=("Arial", 22, "bold")).pack(pady=(20,10))
        ctk.CTkLabel(info_frame, text=f"Matricola: {matricola}", font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(info_frame, text=f"Corso: {corso}", font=("Arial", 16)).pack(pady=5)

        # --- Grafico dettagliato esami ---
        exams_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15, fg_color="#2a2a2a")
        exams_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # Simulazione dati esami
        exam_names = ["Matematica", "Fisica", "Informatica", "Chimica", "Letteratura"]
        exam_scores = [28, 24, 30, 26, 27]
        exam_cfu = [6, 6, 12, 6, 6]

        # Media ponderata
        media_ponderata = sum([s*c for s,c in zip(exam_scores, exam_cfu)]) / sum(exam_cfu)

        # Grafico con matplotlib
        fig = Figure(figsize=(6,4), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(exam_names, exam_scores, color="#e63946")
        ax.set_ylim(0, 30)
        ax.set_title(f"Voti Esami - Media ponderata: {media_ponderata:.2f}", color="white")
        ax.set_ylabel("Voto", color="white")
        ax.set_facecolor("#2a2a2a")
        fig.patch.set_facecolor("#1c1c1c")
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Visualizza grafico in CTkFrame
        canvas_fig = FigureCanvasTkAgg(fig, master=exams_frame)
        canvas_fig.draw()
        canvas_fig.get_tk_widget().pack(pady=20, padx=10)

    def show_libretto(self):
        import tkinter as tk
        from tkinter import ttk
        import customtkinter as ctk
        from PIL import Image, ImageTk

        # Pulisci il content
        for w in self.content.winfo_children():
            w.destroy()

        # Header principale
        ctk.CTkLabel(
            self.content, 
            text="📚 Libretto Esami", 
            font=("Arial", 24, "bold")
        ).pack(pady=(10,20))

        # Frame principale
        libretto_frame = ctk.CTkFrame(self.content, corner_radius=15, fg_color="#2e2e3e")
        libretto_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Icone per intestazioni ---
        self.icons = {
            "exam": ImageTk.PhotoImage(Image.open("assets/icons/book.png").resize((20,20))),
            "vote": ImageTk.PhotoImage(Image.open("assets/icons/star.png").resize((20,20))),
            "cfu": ImageTk.PhotoImage(Image.open("assets/icons/coin.png").resize((20,20))),
            "status": ImageTk.PhotoImage(Image.open("assets/icons/check.png").resize((20,20))),
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

        # --- Treeview senza intestazioni (usiamo solo il body) ---
        cols = ("Nome Esame", "Voto", "CFU", "Stato")
        self.tree = ttk.Treeview(
            libretto_frame,
            columns=cols,
            show="headings",  # nascondiamo i titoli perché li simuliamo noi
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

        # Larghezza colonne
        for col in cols:
            self.tree.column(col, anchor="center", width=200)

        self.tree.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Label media
        self.avg_label = ctk.CTkLabel(self.content, text="", font=("Arial", 15, "bold"))
        self.avg_label.pack(pady=(10,0))

        # Carica dati esami
        self.load_exams()

        # --- Bottoni ---
        btn_frame = ctk.CTkFrame(self.content, corner_radius=10, fg_color="#222233")
        btn_frame.pack(pady=15, padx=20, fill="x")

        ctk.CTkButton(btn_frame, text="➕ Aggiungi", command=self.add_exam,
                    width=150, fg_color="#4da6ff", hover_color="#66b3ff").pack(side="left", padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="✏️ Modifica", command=self.edit_exam,
                    width=150, fg_color="#ffb84d", hover_color="#ffc966").pack(side="left", padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="🗑️ Rimuovi", command=self.remove_exam,
                    width=150, fg_color="#ff4d4d", hover_color="#ff6666").pack(side="left", padx=10, pady=5)



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
        import customtkinter as ctk
        from utils import clear_token  # importa la funzione

        # Finestra modale
        modal = ctk.CTkToplevel(self.master)
        modal.title("Conferma Logout")
        modal.geometry("400x250")
        modal.grab_set()
        modal.resizable(False, False)
        set_app_icon(modal)

        # Titolo
        ctk.CTkLabel(modal, text="⚠️ Sei sicuro di voler uscire?", 
                    font=("Arial", 20, "bold"), text_color="#ff5555").pack(pady=(30, 10))

        # Messaggio
        ctk.CTkLabel(modal, text="Verrai mandato alla pagina di Login.", 
                    font=("Arial", 14), text_color="#ffffff").pack(pady=(5, 20))

        # Funzione di conferma
        def conferma():
            clear_token()  # cancella la sessione salvata
            modal.destroy()
            self.sidebar.destroy()
            self.content.destroy()
            from views.login_view import LoginView
            LoginView(self.master)

        # Pulsanti
        buttons_frame = ctk.CTkFrame(modal, fg_color="transparent")
        buttons_frame.pack(pady=10)

        ctk.CTkButton(buttons_frame, text="✅ Conferma", command=conferma,
                    width=150, fg_color="#e63946", hover_color="#ff4d5a").grid(row=0, column=0, padx=10)

        ctk.CTkButton(buttons_frame, text="❌ Annulla", command=modal.destroy,
                    width=150, fg_color="#888888", hover_color="#aaaaaa").grid(row=0, column=1, padx=10)



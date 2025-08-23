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
        for w in self.content.winfo_children(): w.destroy()
        cols = ("Nome Esame", "Voto", "CFU")
        self.tree = ttk.Treeview(self.content, columns=cols, show="headings", height=15)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(pady=10)
        self.load_exams()

        btn_frame = ctk.CTkFrame(self.content)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Aggiungi", command=self.add_exam).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Modifica", command=self.edit_exam).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Rimuovi", command=self.remove_exam).pack(side="left", padx=5)

    def load_exams(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        exams = get_exams(self.student_id)
        for e in exams: self.tree.insert("", "end", iid=e[0], values=(e[1], e[2], e[3]))

    def add_exam(self):
        nome = simpledialog.askstring("Nuovo Esame", "Nome:")
        voto = simpledialog.askinteger("Voto", "Inserisci voto (18-30):")
        cfu = simpledialog.askinteger("CFU", "Inserisci CFU:")
        if nome and voto and cfu:
            add_exam(self.student_id, nome, voto, cfu)
            self.load_exams()

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

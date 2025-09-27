import customtkinter as ctk
from tkinter import ttk
from controllers.exam_controller import get_exams
from configuration.unigrade_configuration import DISPLAY_30L, NOT_PASSED, PASSED

from views.home.home_view_components.libretto.libretto_view_components.dialogs.add_exam_dialog import (
    AddExamDialog,
)
from views.home.home_view_components.libretto.libretto_view_components.dialogs.edit_exam_dialog import (
    EditExamDialog,
)
from views.home.home_view_components.libretto.libretto_view_components.dialogs.remove_exam_dialog import (
    RemoveExamDialog,
)


class ExamsTable(ctk.CTkFrame):
    def __init__(self, master, student_id, canvas=None):
        super().__init__(master, fg_color="#1c1c1c")
        self.student_id = student_id
        self.canvas = canvas  # serve per il blocco dello scroll globale

        # ------------------------
        # Treeview + Scrollbar
        # ------------------------
        cols = ("Nome Esame", "Voto", "CFU", "Stato")

        # Frame interno
        tree_frame = ctk.CTkFrame(self, fg_color="#2e2e3e", corner_radius=10)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 10))

        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12)

        # Stile moderno
        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#1e1e2f",
            foreground="white",
            fieldbackground="#1e1e2f",
            font=("Arial", 13),
            rowheight=38,
        )
        style.map(
            "Treeview",
            background=[("selected", "#4da6ff")],
            foreground=[("selected", "white")],
        )

        # Colonne
        for col in cols:
            self.tree.column(col, anchor="center", width=200)
            self.tree.heading(col, text=col)

        # Scrollbar verticale
        tree_scroll = ctk.CTkScrollbar(
            tree_frame, orientation="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Alternanza colori righe
        def style_rows(event):
            for i, row in enumerate(self.tree.get_children()):
                if i % 2 == 0:
                    self.tree.item(row, tags=("even",))
                else:
                    self.tree.item(row, tags=("odd",))

        self.tree.tag_configure("even", background="#1e1e2f")
        self.tree.tag_configure("odd", background="#29293f")
        self.tree.bind("<Configure>", style_rows)

        # Blocca lo scroll globale quando il mouse entra nella tree
        if self.canvas:

            def block_global_scroll(event):
                self.canvas.unbind_all("<MouseWheel>")

            def restore_global_scroll(event):
                self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

            self.tree.bind("<Enter>", block_global_scroll)
            self.tree.bind("<Leave>", restore_global_scroll)

        # Label media ponderata
        self.avg_label = ctk.CTkLabel(self, text="", font=("Arial", 15, "bold"))
        self.avg_label.pack(pady=(10, 0))

        # Carica esami dal DB
        self.refresh_table()

    def show_message(self, text, success=True, duration=1500):
        """Mostra un messaggio temporaneo in popup"""
        popup = ctk.CTkToplevel(self)
        popup.overrideredirect(True)  # senza barra titolo
        popup.geometry(f"250x60+{self.winfo_rootx()+50}+{self.winfo_rooty()+50}")
        popup.attributes("-topmost", True)

        fg_color = "#4da6ff" if success else "#ff6666"
        ctk.CTkLabel(
            popup, text=text, font=("Arial", 12, "bold"), fg_color=fg_color
        ).pack(fill="both", expand=True)

        # chiudi automaticamente dopo duration ms
        popup.after(duration, popup.destroy)

    # ------------------------
    # CRUD Methods
    # ------------------------
    def refresh_table(self):
        # svuota la tabella
        self.tree.delete(*self.tree.get_children())

        exams = get_exams(self.student_id)

        self.total_weighted = 0
        self.total_cfu = 0
        self.total_counted_exams = 0

        for e in exams:
            exam_id = e["id"]
            nome = e["nome"]
            voto = e["voto"]
            cfu = e["cfu"]

            # calcola stato e voto da mostrare
            if voto is None or str(voto).strip() == "":
                stato = "In attesa ⏳"
                voto_display = "-"
            else:
                voto_str = str(voto).strip().upper()
                if voto_str in [PASSED, NOT_PASSED]:
                    stato = voto_str + (" ✅" if voto_str == PASSED else " ❌")
                    voto_display = voto_str
                elif voto_str == DISPLAY_30L:
                    stato = "Passato ✅"
                    voto_display = DISPLAY_30L
                    self.total_weighted += 30 * cfu
                    self.total_cfu += cfu
                    self.total_counted_exams += 1
                else:
                    try:
                        voto_num = int(voto_str)
                        if 18 <= voto_num <= 30:
                            stato = "Passato ✅"
                            voto_display = voto_num
                            self.total_weighted += voto_num * cfu
                            self.total_cfu += cfu
                            self.total_counted_exams += 1
                        else:
                            stato = "Non superato ❌"
                            voto_display = voto_num
                    except ValueError:
                        stato = "Valore non valido"
                        voto_display = voto_str

            # inserisci nella TreeView usando id come iid
            self.tree.insert(
                "",
                "end",
                iid=exam_id,
                values=(nome, voto_display, cfu, stato),
            )

        # aggiorna label media ponderata
        self.update_avg()

    def update_avg(self):
        if self.total_cfu > 0:
            media = self.total_weighted / self.total_cfu
            self.avg_label.configure(text=f"📊 Media ponderata: {media:.2f}")
        else:
            self.avg_label.configure(text="📊 Media ponderata: N/A")

    def add_exam(self):
        dialog = AddExamDialog(self, self.student_id)
        self.wait_window(dialog)
        if dialog.result:
            print("DEBUG add_exam: dialog.result =", dialog.result)
            print("DEBUG add_exam: student_id =", self.student_id)

            from controllers.exam_controller import add_exam

            try:
                success = add_exam(self.student_id, **dialog.result)
                if success:
                    self.refresh_table()
                    self.show_message("✅ Esame aggiunto con successo", success=True)
                else:
                    self.show_message(
                        "❌ Errore nell'aggiunta dell'esame", success=False
                    )
            except Exception as e:
                print("DEBUG add_exam ERROR:", e)
                self.show_message("❌ Errore nell'aggiunta dell'esame", success=False)

    def edit_exam(self):
        selected = self.tree.selection()
        if not selected:
            print("DEBUG edit_exam: nessun esame selezionato")
            self.show_message("⚠️ Seleziona un esame da modificare", success=False)
            return
        exam_id = int(selected[0])
        values = self.tree.item(selected[0], "values")
        print("DEBUG edit_exam: selected exam_id =", exam_id)
        print("DEBUG edit_exam: current values =", values)

        dialog = EditExamDialog(self, self.student_id, values)
        self.wait_window(dialog)
        if dialog.result:
            print("DEBUG edit_exam: dialog.result =", dialog.result)

            from controllers.exam_controller import update_exam

            try:
                success = update_exam(exam_id, **dialog.result)
                if success:
                    self.refresh_table()
                    self.show_message("✅ Esame modificato con successo", success=True)
                else:
                    self.show_message(
                        "❌ Errore nella modifica dell'esame", success=False
                    )
            except Exception as e:
                print("DEBUG edit_exam ERROR:", e)
                self.show_message("❌ Errore nella modifica dell'esame", success=False)

    def remove_exam(self):
        selected = self.tree.selection()
        if not selected:
            self.show_message("⚠️ Seleziona un esame da rimuovere", success=False)
            return
        exam_id = int(selected[0])
        values = self.tree.item(selected[0], "values")
        dialog = RemoveExamDialog(self, self.student_id, values)
        self.wait_window(dialog)
        if dialog.confirmed:
            from controllers.exam_controller import remove_exam

            try:
                remove_exam(exam_id)
                self.refresh_table()
                self.show_message("✅ Esame rimosso con successo", success=True)
            except Exception as e:
                print("DEBUG remove_exam ERROR:", e)
                self.show_message("❌ Errore nella rimozione dell'esame", success=False)

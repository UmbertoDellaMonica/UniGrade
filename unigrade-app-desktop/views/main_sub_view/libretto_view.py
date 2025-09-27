import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from controllers.exam_controller import get_exams, add_exam, update_exam, remove_exam
from utils import resource_path, set_app_icon


class LibrettoView(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.master = master
        self.student_id = student_id
        self.pack(fill="both", expand=True)

        # ------------------------
        # Canvas principale + scrollbar
        # ------------------------
        self.canvas = tk.Canvas(self, bg="#1c1c1c", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame scrollabile
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#1c1c1c")
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # Aggiorna scrollregion quando cambia la dimensione del contenuto
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind("<Configure>", self._resize_scrollable_frame)

        # Bind scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows/Mac
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux_up)  # Linux up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux_down)  # Linux down

        # ------------------------
        # Inizializza contenuto principale
        # ------------------------
        self._init_content()

        # Fissa il punto di partenza dello scroll sulla label titolo
        self.scrollable_frame.update_idletasks()
        self.canvas.yview_moveto(0)

    # ------------------------
    # FUNZIONI SCROLL
    # ------------------------
    def _resize_scrollable_frame(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def _on_mousewheel_linux_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def _on_mousewheel_linux_down(self, event):
        self.canvas.yview_scroll(1, "units")

    # ------------------------
    # CONTENUTO PRINCIPALE
    # ------------------------
    def _init_content(self):
        self._init_header()
        self._init_treeview()
        self._init_buttons()

    # ------------------------
    # Header: titolo principale
    # ------------------------
    def _init_header(self):
        self.title_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="📚 Libretto Esami",
            font=("Arial", 24, "bold"),
        )
        self.title_label.pack(pady=(10, 0))

        # Frame libretto
        self.libretto_frame = ctk.CTkFrame(
            self.scrollable_frame, corner_radius=15, fg_color="#2e2e3e"
        )
        self.libretto_frame.pack(fill="both", expand=True, padx=20, pady=(10, 0))

        # Icone header
        self.icons = {
            "exam": ctk.CTkImage(
                light_image=Image.open(resource_path("assets/icons/book.png")),
                dark_image=Image.open(resource_path("assets/icons/book.png")),
                size=(20, 20),
            ),
            "vote": ctk.CTkImage(
                light_image=Image.open(resource_path("assets/icons/star.png")),
                dark_image=Image.open(resource_path("assets/icons/star.png")),
                size=(20, 20),
            ),
            "cfu": ctk.CTkImage(
                light_image=Image.open(resource_path("assets/icons/coin.png")),
                dark_image=Image.open(resource_path("assets/icons/coin.png")),
                size=(20, 20),
            ),
            "status": ctk.CTkImage(
                light_image=Image.open(resource_path("assets/icons/check.png")),
                dark_image=Image.open(resource_path("assets/icons/check.png")),
                size=(20, 20),
            ),
        }

        headers = [
            ("Nome Esame", self.icons["exam"]),
            ("Voto", self.icons["vote"]),
            ("CFU", self.icons["cfu"]),
            ("Stato", self.icons["status"]),
        ]

        # Header personalizzato
        header_frame = ctk.CTkFrame(
            self.libretto_frame, fg_color="#2b2b3d", corner_radius=8
        )
        header_frame.pack(fill="x", pady=(5, 0))
        for text, icon in headers:
            lbl = ctk.CTkLabel(
                header_frame,
                text=f" {text}",
                image=icon,
                compound="left",
                font=("Arial", 14, "bold"),
                padx=10,
            )
            lbl.pack(side="left", expand=True, fill="x", padx=5, pady=5)

    # ------------------------
    # Treeview + Media ponderata (con scrolling interno)
    # ------------------------
    def _init_treeview(self):
        cols = ("Nome Esame", "Voto", "CFU", "Stato")

        # Frame interno con scrollbar verticale per la TreeView
        tree_frame = ctk.CTkFrame(
            self.libretto_frame, fg_color="#2e2e3e", corner_radius=10
        )
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 10))

        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="", height=12)

        # Stile tabella moderno
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

        # Alternanza colore righe
        def style_rows(event):
            for i, row in enumerate(self.tree.get_children()):
                if i % 2 == 0:
                    self.tree.item(row, tags=("even",))
                else:
                    self.tree.item(row, tags=("odd",))

        self.tree.tag_configure("even", background="#1e1e2f")
        self.tree.tag_configure("odd", background="#29293f")
        self.tree.bind("<Configure>", style_rows)

        # Blocca scroll globale quando il mouse è sopra la TreeView
        def block_global_scroll(event):
            self.canvas.unbind_all("<MouseWheel>")

        def restore_global_scroll(event):
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.tree.bind("<Enter>", block_global_scroll)
        self.tree.bind("<Leave>", restore_global_scroll)

        # Label media ponderata
        self.avg_label = ctk.CTkLabel(
            self.scrollable_frame, text="", font=("Arial", 15, "bold")
        )
        self.avg_label.pack(pady=(10, 0))

        # Carica dati esami
        self.load_exams()

    # ------------------------
    # Bottoni Aggiungi/Modifica/Rimuovi
    # ------------------------
    def _init_buttons(self):
        btn_frame = ctk.CTkFrame(
            self.scrollable_frame, corner_radius=10, fg_color="#222233"
        )
        btn_frame.pack(pady=15, padx=20, fill="x")

        ctk.CTkButton(
            btn_frame,
            text="➕ Aggiungi",
            command=self.add_exam,
            width=150,
            fg_color="#4da6ff",
            hover_color="#66b3ff",
        ).pack(side="left", padx=10, pady=5)

        ctk.CTkButton(
            btn_frame,
            text="✏️ Modifica",
            command=self.edit_exam,
            width=150,
            fg_color="#ffb84d",
            hover_color="#ffc966",
        ).pack(side="left", padx=10, pady=5)

        ctk.CTkButton(
            btn_frame,
            text="🗑️ Rimuovi",
            command=self.remove_exam,
            width=150,
            fg_color="#ff4d4d",
            hover_color="#ff6666",
        ).pack(side="left", padx=10, pady=5)

    def load_exams(self):
        # svuota la tabella
        self.tree.delete(*self.tree.get_children())

        exams = get_exams(self.student_id)
        self.total_weighted = 0  # 🔑 salva come attributo
        self.total_cfu = 0  # 🔑 idem
        self.total_counted_exams = 0

        for e in exams:
            eid = e["id"]
            nome = e["nome"]
            voto = e["voto"]
            cfu = e["cfu"]

            if voto is None or str(voto).strip() == "":
                stato = "In attesa ⏳"
                voto_display = "-"
            else:
                voto_str = str(voto).strip().upper()
                if voto_str in ["SUPERATO", "NON SUPERATO"]:
                    stato = voto_str + (" ✅" if voto_str == "SUPERATO" else " ❌")
                    voto_display = voto_str
                elif voto_str == "30L":
                    stato = "Passato ✅"
                    voto_display = "30L"
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

            self.tree.insert(
                "", "end", iid=eid, values=(nome, voto_display, cfu, stato)
            )

        # 🔑 aggiorna label
        self.update_avg()

    def update_avg(self):
        if self.total_cfu > 0:
            media = self.total_weighted / self.total_cfu
            self.avg_label.configure(text=f"📊 Media ponderata: {media:.2f}")
        else:
            self.avg_label.configure(text="📊 Media ponderata: N/A")

    def add_exam(self):
        # finestra modale
        modal = ctk.CTkToplevel(self.master)
        modal.title("Aggiungi Nuovo Esame")
        modal.geometry("400x500")
        modal.grab_set()
        modal.resizable(False, False)
        set_app_icon(modal)

        # Titolo
        ctk.CTkLabel(modal, text="📚 Nuovo Esame", font=("Arial", 20, "bold")).pack(
            pady=(20, 15)
        )

        # Frame campi
        fields_frame = ctk.CTkFrame(modal, corner_radius=15, fg_color="#2e2e3e")
        fields_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Nome esame
        ctk.CTkLabel(fields_frame, text="Nome Esame", font=("Arial", 14)).grid(
            row=0, column=0, sticky="e", padx=10, pady=10
        )
        entry_nome = ctk.CTkEntry(fields_frame, width=200)
        entry_nome.grid(row=0, column=1, padx=10, pady=10)

        # ComboBox per voto con i valori descritti
        ctk.CTkLabel(fields_frame, text="Voto", font=("Arial", 14)).grid(
            row=1, column=0, sticky="e", padx=10, pady=10
        )
        voti_possibili = (
            ["", "SUPERATO", "NON SUPERATO"] + [str(i) for i in range(18, 31)] + ["30L"]
        )
        combo_voto = ctk.CTkComboBox(fields_frame, values=voti_possibili, width=120)
        combo_voto.set("")  # default vuoto
        combo_voto.grid(row=1, column=1, padx=10, pady=10)

        # CFU
        ctk.CTkLabel(fields_frame, text="CFU", font=("Arial", 14)).grid(
            row=2, column=0, sticky="e", padx=10, pady=10
        )
        entry_cfu = ctk.CTkEntry(fields_frame, width=100)
        entry_cfu.grid(row=2, column=1, padx=10, pady=10)

        # Label messaggi in tempo reale
        msg_label = ctk.CTkLabel(
            modal, text="", font=("Arial", 12), text_color="#ff6666"
        )
        msg_label.pack(pady=(5, 0))

        # Funzione conferma
        def conferma():
            nome = entry_nome.get().strip()
            voto_text = combo_voto.get().strip()
            cfu_text = entry_cfu.get().strip()

            # validazioni
            if not nome:
                msg_label.configure(text="Inserisci il nome dell'esame!")
                return

            # CFU ok
            try:
                cfu = int(cfu_text)
                if cfu <= 0:
                    msg_label.configure(text="CFU deve essere un numero positivo!")
                    return
            except ValueError:
                msg_label.configure(text="CFU deve essere un numero!")
                return

            # Voto processing
            voto = None
            voto_up = voto_text.upper()
            if voto_up in ["SUPERATO", "NON SUPERATO", "30L"]:
                voto = voto_up
            elif voto_text == "":
                voto = None
            else:
                # numero
                try:
                    vn = int(voto_text)
                    if vn < 18 or vn > 30:
                        msg_label.configure(
                            text="Voto numerico deve essere tra 18 e 30 o 30L!"
                        )
                        return
                    voto = vn
                except ValueError:
                    msg_label.configure(text="Voto non valido!")
                    return

            # Chiamata controller
            success = add_exam(self.student_id, nome, voto, cfu)
            if success:
                self.load_exams()
                modal.destroy()

                # Messaggio di successo
                msg = ctk.CTkLabel(
                    self.master,
                    text="✅ Esame aggiunto!",
                    font=("Arial", 14, "bold"),
                    text_color="#4dd17f",
                )
                msg.place(relx=0.5, rely=0.95, anchor="s")
                self.master.after(2000, msg.destroy)
            else:
                msg_label.configure(text=f"L'esame '{nome}' è già presente!")

        # Pulsanti
        ctk.CTkButton(
            modal,
            text="Aggiungi",
            command=conferma,
            width=180,
            fg_color="#4da6ff",
            hover_color="#66b3ff",
        ).pack(pady=(20, 15))
        ctk.CTkButton(
            modal,
            text="Annulla",
            command=modal.destroy,
            width=180,
            fg_color="#888888",
            hover_color="#aaaaaa",
        ).pack(pady=(0, 15))

    def edit_exam(self):
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
        ctk.CTkLabel(modal, text="✏️ Modifica Esame", font=("Arial", 20, "bold")).pack(
            pady=(20, 15)
        )

        # Frame campi
        fields_frame = ctk.CTkFrame(modal, corner_radius=15, fg_color="#2e2e3e")
        fields_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Nome esame
        ctk.CTkLabel(fields_frame, text="Nome Esame", font=("Arial", 14)).grid(
            row=0, column=0, sticky="e", padx=10, pady=10
        )
        entry_nome = ctk.CTkEntry(fields_frame, width=200)
        entry_nome.insert(0, vals[0])
        entry_nome.grid(row=0, column=1, padx=10, pady=10)

        # Voto (combo)
        ctk.CTkLabel(fields_frame, text="Voto", font=("Arial", 14)).grid(
            row=1, column=0, sticky="e", padx=10, pady=10
        )
        voti_possibili = (
            ["", "SUPERATO", "NON SUPERATO"] + [str(i) for i in range(18, 31)] + ["30L"]
        )
        combo_voto = ctk.CTkComboBox(fields_frame, values=voti_possibili, width=120)
        combo_voto.set(str(vals[1]))  # precompila, vals[1] è voto_display
        combo_voto.grid(row=1, column=1, padx=10, pady=10)

        # CFU
        ctk.CTkLabel(fields_frame, text="CFU", font=("Arial", 14)).grid(
            row=2, column=0, sticky="e", padx=10, pady=10
        )
        entry_cfu = ctk.CTkEntry(fields_frame, width=100)
        entry_cfu.insert(0, vals[2])
        entry_cfu.grid(row=2, column=1, padx=10, pady=10)

        # Label messaggi
        msg_label = ctk.CTkLabel(
            modal, text="", font=("Arial", 12), text_color="#ff6666"
        )
        msg_label.pack(pady=(5, 0))

        # Funzione conferma
        def conferma():
            nome = entry_nome.get().strip()
            voto_text = combo_voto.get().strip()
            cfu_text = entry_cfu.get().strip()

            if not nome:
                msg_label.configure(text="Inserisci il nome dell'esame!")
                return

            try:
                cfu = int(cfu_text)
                if cfu <= 0:
                    msg_label.configure(text="CFU deve essere un numero positivo!")
                    return
            except ValueError:
                msg_label.configure(text="CFU deve essere un numero valido!")
                return

            voto_up = voto_text.upper()
            if voto_up in ["SUPERATO", "NON SUPERATO", "30L"]:
                voto = voto_up
            elif voto_text == "":
                voto = None
            else:
                try:
                    vn = int(voto_text)
                    if vn < 18 or vn > 30:
                        msg_label.configure(
                            text="Voto numerico deve essere tra 18 e 30 o 30L!"
                        )
                        return
                    voto = vn
                except ValueError:
                    msg_label.configure(text="Voto non valido!")
                    return

            update_exam(eid, nome, voto, cfu)
            self.load_exams()
            modal.destroy()

            success = ctk.CTkLabel(
                self.master,
                text="✅ Esame modificato!",
                font=("Arial", 14, "bold"),
                text_color="#4dd17f",
            )
            success.place(relx=0.5, rely=0.95, anchor="s")
            self.master.after(2000, success.destroy)

        # Pulsanti
        ctk.CTkButton(
            modal,
            text="Salva Modifiche",
            command=conferma,
            width=180,
            fg_color="#4da6ff",
            hover_color="#66b3ff",
        ).pack(pady=(20, 15))
        ctk.CTkButton(
            modal,
            text="Annulla",
            command=modal.destroy,
            width=180,
            fg_color="#888888",
            hover_color="#aaaaaa",
        ).pack(pady=(0, 15))

    def remove_exam(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Attenzione", "Seleziona un esame da eliminare!")
            return

        eid = sel[0]
        vals = self.tree.item(eid, "values")

        modal = ctk.CTkToplevel(self.master)
        modal.title("Conferma Eliminazione")
        modal.geometry("400x250")
        modal.grab_set()
        modal.resizable(False, False)
        set_app_icon(modal)

        ctk.CTkLabel(
            modal,
            text="⚠️ Eliminare Esame?",
            font=("Arial", 20, "bold"),
            text_color="#ff5555",
        ).pack(pady=(20, 10))

        info_text = f"Nome: {vals[0]}\nVoto: {vals[1]}\nCFU: {vals[2]}"
        ctk.CTkLabel(
            modal, text=info_text, font=("Arial", 14), text_color="#ffffff"
        ).pack(pady=(5, 20))

        def conferma_del():
            remove_exam(eid)
            self.load_exams()
            modal.destroy()
            success = ctk.CTkLabel(
                self.master,
                text="🗑️ Esame eliminato!",
                font=("Arial", 14, "bold"),
                text_color="#ff6666",
            )
            success.place(relx=0.5, rely=0.95, anchor="s")
            self.master.after(2000, success.destroy)

        buttons_frame = ctk.CTkFrame(modal, fg_color="transparent")
        buttons_frame.pack(pady=10)

        ctk.CTkButton(
            buttons_frame,
            text="✅ Conferma",
            command=conferma_del,
            width=150,
            fg_color="#e63946",
            hover_color="#ff4d5a",
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            buttons_frame,
            text="❌ Annulla",
            command=modal.destroy,
            width=150,
            fg_color="#888888",
            hover_color="#aaaaaa",
        ).grid(row=0, column=1, padx=10)

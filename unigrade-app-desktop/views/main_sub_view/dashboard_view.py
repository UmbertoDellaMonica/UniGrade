import customtkinter as ctk
import tkinter as tk
from controllers.student_controller import get_student
from controllers.exam_controller import get_exams
from views.main_sub_view.avatar_view import AvatarComponent
from PIL import Image
from configuration.unigrade_configuration import resource_path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import mplcursors


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.student_id = student_id

        # --- Dati studente ---
        self.student = get_student(student_id) or {
            "nome": "N/D",
            "cognome": "N/D",
            "corso": "N/D",
            "matricola": "N/D",
            "avatar_path": None,
        }

        # --- Canvas principale con scrollbar ---
        self._init_scrollable_canvas()

        # --- Header row: Avatar + Info Studente + Refresh ---
        self._init_header_row()

        # --- Exam Chart ---
        self._init_exam_chart()

        # --- Dummy content aggiuntivo ---
        # self._populate_dummy_elements()

    # ------------------------
    # Canvas scrollabile
    # ------------------------
    def _init_scrollable_canvas(self):
        self.canvas = tk.Canvas(self, bg="#1c1c1c", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#1c1c1c")
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind("<Configure>", self._resize_scrollable_frame)

        # Bind scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux_up)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux_down)

    def _resize_scrollable_frame(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def _on_mousewheel_linux_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def _on_mousewheel_linux_down(self, event):
        self.canvas.yview_scroll(1, "units")

    # ------------------------
    # Header Row: Avatar + Info + Refresh
    # ------------------------
    def _init_header_row(self):
        self.header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1c1c1c")
        self.header_frame.pack(fill="x", padx=20, pady=0)

        # Avatar a sinistra, allineato in alto
        self._init_avatar()
        self.avatar_component.avatar_frame.pack(side="left", padx=(0, 20), anchor="n")

        # Info Studente al centro, allineato in alto
        self._init_student_info()
        self.info_frame.pack(
            side="left", fill="both", expand=True, padx=(0, 20), pady=0, anchor="n"
        )

        # Refresh button a destra, allineato in alto
        self._init_refresh_button()
        self.refresh_btn.pack(side="right", padx=10, pady=0, anchor="n")

    # --- Avatar Component ---
    def _init_avatar(self):
        self.avatar_component = AvatarComponent(
            self.header_frame,
            self.student_id,
            avatar_path=(
                self.student["avatar_path"]
                if self.student and "avatar_path" in self.student.keys()
                else None
            ),
        )
        self.avatar_component.avatar_frame.pack(side="left", padx=(0, 20))

    # --- Info Studente ---
    def _init_student_info(self):
        self.info_frame = ctk.CTkFrame(
            self.header_frame,
            corner_radius=20,
            fg_color="#2a2a2a",
            border_width=2,
            border_color="#4da6ff",
        )
        self.info_frame.pack(
            side="left", fill="both", expand=True, padx=(0, 20), pady=5
        )

        # Titolo
        ctk.CTkLabel(
            self.info_frame,
            text="Informazioni Studente",
            font=("Arial", 20, "bold"),
            text_color="#4da6ff",
        ).pack(pady=(15, 15))

        # Dettagli + statistiche
        details_frame = ctk.CTkFrame(
            self.info_frame, fg_color="#1c1c1c", corner_radius=15
        )
        details_frame.pack(fill="both", padx=15, pady=(0, 15))

        # Info di base
        for label, value in [
            ("🧑 Nome", self.student["nome"]),
            ("👤 Cognome", self.student["cognome"]),
            ("🎓 Corso", self.student["corso"]),
            ("🆔 Matricola", self.student["matricola"]),
        ]:
            ctk.CTkLabel(
                details_frame, text=f"{label}: {value}", font=("Arial", 14)
            ).pack(anchor="w", pady=5, padx=10)

        # Statistiche esami
        self._populate_student_stats(details_frame)

    def _populate_student_stats(self, parent_frame):
        exams = get_exams(self.student_id)
        numeric_exams, cfu_acquisiti, cfu_totali_piano = [], 0, 0
        count_superati, count_non_superati = 0, 0

        for e in exams:
            voto_raw, cfu_raw = e[2], e[3]
            try:
                cfu = int(cfu_raw)
                cfu_totali_piano += cfu
            except:
                continue
            voto_str = str(voto_raw).strip().upper()
            if voto_str == "NON SUPERATO":
                count_non_superati += 1
                continue
            if voto_str == "SUPERATO":
                count_superati += 1
                cfu_acquisiti += cfu
                continue
            if voto_str.endswith("L") and voto_str[:-1].isdigit():
                voto = int(voto_str[:-1])
            elif voto_str.isdigit():
                voto = int(voto_str)
            else:
                continue
            count_superati += 1
            cfu_acquisiti += cfu
            numeric_exams.append((voto, cfu))

        totale_cfu_numeric = sum(c[1] for c in numeric_exams)
        media = (
            sum(v * c for v, c in numeric_exams) / totale_cfu_numeric
            if totale_cfu_numeric
            else 0
        )
        voto_iniziale_laurea = round(media * 110 / 30) if numeric_exams else "N/A"

        stats = [
            ("📚 Esami superati", count_superati),
            ("❌ Esami non superati", count_non_superati),
            ("🕒 Esami da sostenere", count_non_superati),
            ("🎯 Media ponderata", f"{media:.2f}" if numeric_exams else "N/A"),
            ("💎 CFU acquisiti", f"{cfu_acquisiti}/{cfu_totali_piano}"),
            ("🏆 Voto Iniziale di Laurea", voto_iniziale_laurea),
        ]

        # Stile uniforme con info di base
        for label, val in stats:
            ctk.CTkLabel(
                parent_frame,
                text=f"{label}: {val}",
                font=("Arial", 14),
                anchor="w",
                padx=10,
            ).pack(fill="x", pady=5)

    # --- Refresh Button ---
    def _init_refresh_button(self):
        # Usare CTkImage per compatibilità HighDPI
        self.refresh_ctk_image = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/icons/reload.png")),
            dark_image=Image.open(resource_path("assets/icons/reload.png")),
            size=(28, 28),
        )

        self.refresh_btn = ctk.CTkButton(
            self.header_frame,
            image=self.refresh_ctk_image,
            text="",
            width=50,
            height=50,
            fg_color="#4da6ff",
            hover_color="#6ab0ff",
            corner_radius=25,
            command=self._update_dashboard,
        )
        self.refresh_btn.pack(side="right", padx=10, pady=10)

    # ------------------------
    # Exam Chart
    # ------------------------
    def _init_exam_chart(self):
        self.exam_chart_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=15,
            fg_color="#2a2a2a",
        )
        # Aumentiamo il padding verticale per dare più spazio
        self.exam_chart_frame.pack(fill="both", padx=20, pady=80, expand=True)

        exams = get_exams(self.student_id)
        valid_exams = []
        exam_labels = []

        for i, e in enumerate(exams):
            nome_raw, voto_raw = e[1], e[2]
            if not voto_raw:
                continue
            voto_str = str(voto_raw).strip().upper()
            if voto_str.endswith("L") and voto_str[:-1].isdigit():
                voto = int(voto_str[:-1])
            elif voto_str.isdigit():
                voto = int(voto_str)
            else:
                continue

            valid_exams.append((i + 1, voto))
            # Genera acronimo se troppo lungo
            if len(nome_raw) > 15:
                acr = "".join(word[0].upper() for word in nome_raw.split())
            else:
                acr = nome_raw
            exam_labels.append((acr, nome_raw))

        if not valid_exams:
            text = (
                "Nessun esame inserito!"
                if not exams
                else "Nessun voto numerico disponibile!"
            )
            ctk.CTkLabel(
                self.exam_chart_frame, text=text, font=("Arial", 16), text_color="white"
            ).pack(pady=20)
            return

        exam_indices, exam_scores = zip(*valid_exams)
        # Aumentiamo l'altezza del grafico matplotlib
        fig = plt.Figure(figsize=(14, 10), dpi=100)
        ax = fig.add_subplot(111)

        colors = [
            "#e63946" if v < 24 else "#f1c40f" if v < 28 else "#2ecc71"
            for v in exam_scores
        ]
        ax.scatter(exam_indices, exam_scores, color=colors, s=140)
        ax.plot(exam_indices, exam_scores, color="#e63946", linewidth=2, alpha=0.6)

        ax.set_ylim(18, 31)
        ax.set_title("Andamento voti", color="white")
        ax.set_xlabel("Esami", color="white")
        ax.set_ylabel("Voto", color="white")
        ax.set_xticks(exam_indices)
        ax.set_xticklabels(
            [a[0] for a in exam_labels],
            rotation=45,
            ha="right",
            fontsize=12,
            color="white",
        )
        ax.tick_params(axis="y", colors="white", labelsize=12)
        ax.set_facecolor("#2a2a2a")
        fig.patch.set_facecolor("#1c1c1c")

        canvas_fig = FigureCanvasTkAgg(fig, master=self.exam_chart_frame)
        canvas_fig.draw()
        canvas_fig.get_tk_widget().pack(fill="both", expand=True, pady=20, padx=10)

        # Tooltip con nome completo
        cursor = mplcursors.cursor(ax, hover=True)

        def show_full_name(sel):
            index = int(sel.index)
            nome_completo = exam_labels[index][1]
            sel.annotation.set_text(f"{nome_completo}\nVoto: {exam_scores[index]}")

        cursor.connect("add", show_full_name)

    # ------------------------
    # Dummy elementi aggiuntivi
    # ------------------------
    def _populate_dummy_elements(self):
        for i in range(10):
            frame = ctk.CTkFrame(
                self.scrollable_frame, corner_radius=10, fg_color="#333"
            )
            frame.pack(fill="x", padx=20, pady=10)
            ctk.CTkLabel(
                frame, text=f"Elemento fittizio {i+1}", font=("Arial", 16)
            ).pack(padx=10, pady=10)

    # ------------------------
    # Aggiornamento dashboard
    # ------------------------
    def _update_dashboard(self):
        self.destroy()
        DashboardView(self.master, self.student_id)

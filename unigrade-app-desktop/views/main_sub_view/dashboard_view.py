import customtkinter as ctk
import tkinter as tk
import mplcursors
from controllers.student_controller import get_student
from controllers.exam_controller import get_exams
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from utils import resource_path
from views.main_sub_view.avatar_view import AvatarComponent


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.student_id = student_id
        self.refreshing = False

        # --- Dati studente ---
        self.student = get_student(student_id) or {
            "nome": "N/D",
            "cognome": "N/D",
            "corso": "N/D",
            "matricola": "N/D",
            "avatar_path": None,
        }

        # --- Canvas scrollabile globale ---
        self.canvas = tk.Canvas(self, bg="#1c1c1c", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#1c1c1c")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Scroll globale cross-platform
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows / Mac
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # Linux scroll down

        # --- Layout principale ---
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.center_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.center_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
        self.center_frame.grid_columnconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(1, weight=2)
        self.center_frame.grid_columnconfigure(2, weight=1)

        # --- Componenti ---
        self.avatar_component = AvatarComponent(
            self.center_frame,
            self.student_id,
            avatar_path=(
                self.student["avatar_path"]
                if self.student and "avatar_path" in self.student.keys()
                else None
            ),
        )
        self.init_student_info()
        self.init_refresh_button()
        self.init_exam_chart()

        # --- Posizionamento ---
        self.avatar_component.avatar_frame.grid(row=0, column=0, sticky="nsew")
        self.info_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.refresh_btn.grid(row=0, column=2, sticky="ne", padx=20, pady=20)
        self.exam_chart_frame.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=20, pady=30
        )

        # --- Animazioni avatar hover ---
        self.avatar_component.avatar_img_label.bind("<Enter>", self._avatar_hover_enter)
        self.avatar_component.avatar_img_label.bind("<Leave>", self._avatar_hover_leave)

    # ------------------------
    # SCROLL DEL MOUSE GLOBALE
    # ------------------------
    def _on_mousewheel(self, event):
        delta = 0
        if event.num == 5 or event.delta < 0:
            delta = 1
        elif event.num == 4 or event.delta > 0:
            delta = -1
        self.canvas.yview_scroll(delta, "units")

    # ------------------------
    # AVATAR HOVER ANIMATION
    # ------------------------
    def _avatar_hover_enter(self, event):
        self.avatar_component.avatar_img_label.configure(fg_color="#4da6ff")

    def _avatar_hover_leave(self, event):
        self.avatar_component.avatar_img_label.configure(fg_color="#444")

    # ------------------------
    # INFO STUDENTE + VOTO INIZIALE DI LAUREA
    # ------------------------
    def init_student_info(self):
        self.info_frame = ctk.CTkFrame(
            self.center_frame,
            corner_radius=20,
            fg_color="#2a2a2a",
            border_width=2,
            border_color="#4da6ff",
        )
        self.info_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        nome_completo = f"{self.student['nome']} {self.student['cognome']}"
        ctk.CTkLabel(
            self.info_frame, text=nome_completo, font=("Arial", 26, "bold")
        ).pack(pady=(20, 5))
        ctk.CTkLabel(
            self.info_frame,
            text=f"{self.student['corso']}",
            font=("Arial", 18, "italic"),
            text_color="#4da6ff",
        ).pack(pady=(0, 15))

        # --- Riassunto esami con cards animate ---
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
            if totale_cfu_numeric > 0
            else 0
        )

        # --- Calcolo Voto Iniziale di Laurea (VIL) proporzionale 110/30 ---
        voto_iniziale_laurea = round(media * 110 / 30) if numeric_exams else "N/A"

        # --- Cards ---
        stats = [
            ("📚 Esami superati", count_superati),
            ("❌ Esami non superati", count_non_superati),
            ("🕒 Esami da sostenere", count_non_superati),
            ("🎯 Media ponderata", f"{media:.2f}" if numeric_exams else "N/A"),
            ("💎 CFU acquisiti", f"{cfu_acquisiti}/{cfu_totali_piano}"),
            ("🏆 Voto Iniziale di Laurea", voto_iniziale_laurea),
        ]

        for title, val in stats:
            card = ctk.CTkFrame(self.info_frame, corner_radius=10, fg_color="#333")
            card.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(card, text=f"{title}: {val}", font=("Arial", 16)).pack(pady=5)

    # ------------------------
    # REFRESH BUTTON E ANIMAZIONE
    # ------------------------
    def init_refresh_button(self):
        self.refresh_frame = ctk.CTkFrame(
            self.center_frame, corner_radius=10, fg_color="transparent"
        )
        self.refresh_frame.grid(row=0, column=2, sticky="ne", padx=20, pady=20)

        self.refresh_img_orig = Image.open(
            resource_path("assets/icons/reload.png")
        ).resize((24, 24))
        self.refresh_photo = ImageTk.PhotoImage(self.refresh_img_orig)

        self.refresh_btn = ctk.CTkButton(
            self.refresh_frame,
            image=self.refresh_photo,
            text="",
            width=40,
            height=40,
            fg_color="#444444",
            hover_color="#666666",
            corner_radius=20,
            command=self.refresh_content,
        )
        self.refresh_btn.pack()

    def animate_refresh(self, angle=0):
        if not getattr(self, "refreshing", False):
            return
        rotated = self.refresh_img_orig.rotate(angle)
        self.refresh_photo = ImageTk.PhotoImage(rotated)
        self.refresh_btn.configure(image=self.refresh_photo)
        self.after(50, lambda: self.animate_refresh(angle + 15))

    def refresh_content(self):
        if getattr(self, "refreshing", False):
            return
        self.refreshing = True
        self.animate_refresh()
        self.student = get_student(self.student_id) or self.student
        for w in self.center_frame.winfo_children():
            w.destroy()
        self.avatar_component = AvatarComponent(
            self.center_frame,
            self.student_id,
            avatar_path=(
                self.student["avatar_path"]
                if self.student and "avatar_path" in self.student.keys()
                else None
            ),
        )
        self.init_student_info()
        self.init_refresh_button()
        self.init_exam_chart()
        self.after(1000, lambda: setattr(self, "refreshing", False))

    # ------------------------
    # GRAFICO ESAMI CON COLORI DINAMICI E TOOLTIP
    # ------------------------
    def init_exam_chart(self):
        self.exam_chart_frame = ctk.CTkFrame(
            self.center_frame,
            corner_radius=15,
            fg_color="#2a2a2a",
            height=600,  # aumento altezza
        )
        self.exam_chart_frame.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=20, pady=30
        )

        exams = get_exams(self.student_id)
        valid_exams = []

        for i, e in enumerate(exams):
            voto_raw = e[2]
            if not voto_raw:
                continue
            voto_str = str(voto_raw).strip().upper()
            if voto_str.endswith("L") and voto_str[:-1].isdigit():
                voto = int(voto_str[:-1])
                valid_exams.append((i + 1, voto))
            elif voto_str.isdigit():
                voto = int(voto_str)
                valid_exams.append((i + 1, voto))

        if not exams or not valid_exams:
            text = (
                "Nessun esame inserito!"
                if not exams
                else "Nessun voto numerico disponibile!"
            )
            ctk.CTkLabel(self.exam_chart_frame, text=text, font=("Arial", 16)).pack(
                pady=20
            )
            return

        exam_indices, exam_scores = zip(*valid_exams)
        fig = Figure(figsize=(12, 8), dpi=100)  # altezza figura aumentata da 6 a 8
        ax = fig.add_subplot(111)
        colors = [
            "#e63946" if v < 24 else "#f1c40f" if v < 28 else "#2ecc71"
            for v in exam_scores
        ]
        ax.scatter(
            exam_indices, exam_scores, color=colors, s=120
        )  # punti leggermente più grandi
        ax.plot(exam_indices, exam_scores, color="#e63946", linewidth=2, alpha=0.6)
        ax.set_ylim(18, 31)
        ax.set_title("Andamento voti", color="white")
        ax.set_xlabel("Esami", color="white")
        ax.set_ylabel("Voto", color="white")
        ax.set_xticks(exam_indices)
        ax.set_xticklabels(
            exam_indices, rotation=45, ha="right", fontsize=12, color="white"
        )
        ax.tick_params(axis="y", colors="white", labelsize=12)
        ax.set_facecolor("#2a2a2a")
        fig.patch.set_facecolor("#1c1c1c")

        canvas_fig = FigureCanvasTkAgg(fig, master=self.exam_chart_frame)
        canvas_fig.draw()
        canvas_fig.get_tk_widget().pack(fill="both", expand=True, pady=20, padx=10)

        # Tooltip voti interattivi
        cursor = mplcursors.cursor(ax, hover=True)
        cursor.connect(
            "add",
            lambda sel: sel.annotation.set_text(f"Voto: {exam_scores[sel.index]}"),
        )

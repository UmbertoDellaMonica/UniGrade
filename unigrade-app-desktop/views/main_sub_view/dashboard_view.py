import customtkinter as ctk
import tkinter as tk
from controllers.student_controller import get_student, update_student_avatar
from controllers.exam_controller import get_exams
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk, ImageDraw
from customtkinter import CTkImage

from tkinter import filedialog
from utils import resource_path


class AvatarComponent:
    """Gestione caricamento e visualizzazione avatar studente"""

    def __init__(self, parent_frame, student_id, avatar_path=None):
        self.parent_frame = parent_frame
        self.student_id = student_id
        self.avatar_path = avatar_path  # recuperato da DB
        self.avatar_img = None

        self.init_avatar_frame()
        if self.avatar_path:
            self.display_avatar(self.avatar_path)

    def init_avatar_frame(self):
        self.avatar_frame = ctk.CTkFrame(
            self.parent_frame, corner_radius=20, fg_color="#2a2a2a"
        )
        self.avatar_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.avatar_label = ctk.CTkLabel(
            self.avatar_frame,
            text="Icona Avatar",
            font=("Arial", 16, "bold"),
            text_color="#4da6ff",
            fg_color="#1c1c1c",
            corner_radius=10,
            padx=10,
            pady=5,
        )
        self.avatar_label.grid(row=0, column=0, pady=(15, 10))

        self.avatar_img_label = ctk.CTkLabel(
            self.avatar_frame,
            text="(clicca per caricare foto)",
            width=180,
            height=180,
            fg_color="#444",
            corner_radius=90,
        )
        self.avatar_img_label.grid(row=1, column=0, pady=10)
        self.avatar_img_label.bind("<Button-1>", self.upload_avatar)

    def display_avatar(self, path):
        img = Image.open(path)
        max_size = 180
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)

        img_circle = Image.new("RGBA", img.size)
        img_circle.paste(img, (0, 0), mask=mask)

        self.avatar_img = CTkImage(
            light_image=img_circle, dark_image=img_circle, size=(180, 180)
        )
        self.avatar_img_label.configure(image=self.avatar_img, text="")

    def upload_avatar(self, event=None):
        file_path = filedialog.askopenfilename(
            title="Seleziona immagine",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")],
        )
        if not file_path:
            return

        self.avatar_path = file_path
        self.display_avatar(file_path)
        update_student_avatar(self.student_id, file_path)


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.student_id = student_id
        self.refreshing = False

        self.student = get_student(student_id) or {
            "nome": "N/D",
            "cognome": "N/D",
            "corso": "N/D",
            "matricola": "N/D",
            "avatar_path": None,  # recupero percorso avatar
        }

        # --- Canvas scrollabile ---
        self.canvas = tk.Canvas(self, bg="#1c1c1c", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#1c1c1c")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind(
            "<Enter>",
            lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel),
        )
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

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

    # ------------------------
    # SCROLL DEL MOUSE
    # ------------------------
    def _on_mousewheel(self, event):
        delta = int(-1 * (event.delta / 120))
        self.canvas.yview_scroll(delta, "units")

    # ------------------------
    # INFO STUDENTE
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

        # Riassunto esami
        exams = get_exams(self.student_id)
        total_cfu = 0
        numeric_exams = []

        for e in exams:
            voto_raw, cfu_raw = e[2], e[3]

            try:
                cfu = int(cfu_raw)
                total_cfu += cfu
            except (ValueError, TypeError):
                continue

            if voto_raw is None:
                continue

            voto_str = str(voto_raw).strip().upper()
            if voto_str.endswith("L") and voto_str[:-1].isdigit():
                voto = int(voto_str[:-1])
                numeric_exams.append((voto, cfu))
            elif voto_str.isdigit():
                voto = int(voto_str)
                numeric_exams.append((voto, cfu))

        totale_cfu_numeric = sum(c[1] for c in numeric_exams)
        media = (
            sum(v * c for v, c in numeric_exams) / totale_cfu_numeric
            if totale_cfu_numeric > 0
            else 0
        )

        summary_frame = ctk.CTkFrame(self.info_frame, corner_radius=10, fg_color="#333")
        summary_frame.pack(fill="x", padx=20, pady=(15, 25))

        ctk.CTkLabel(
            summary_frame,
            text=f"📚 Esami completati: {len(numeric_exams)}",
            font=("Arial", 16),
        ).pack(pady=5)
        ctk.CTkLabel(
            summary_frame,
            text=(
                f"🎯 Media ponderata: {media:.2f}"
                if numeric_exams
                else "🎯 Media ponderata: N/A"
            ),
            font=("Arial", 16),
        ).pack(pady=5)
        ctk.CTkLabel(
            summary_frame,
            text=f"💎 CFU totali: {total_cfu}/{sum(e[3] for e in exams if e[3] is not None)}",
            font=("Arial", 16),
        ).pack(pady=5)

    # ------------------------
    # REFRESH BUTTON
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
        for w in self.center_frame.winfo_children():
            w.destroy()
        self.avatar_component = AvatarComponent(self.center_frame, self.student_id)
        self.init_student_info()
        self.init_refresh_button()
        self.init_exam_chart()
        self.after(1000, lambda: setattr(self, "refreshing", False))

    # ------------------------
    # GRAFICO ESAMI
    # ------------------------
    def init_exam_chart(self):
        self.exam_chart_frame = ctk.CTkFrame(
            self.center_frame, corner_radius=15, fg_color="#2a2a2a", height=400
        )
        self.exam_chart_frame.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=20, pady=30
        )

        exams = get_exams(self.student_id)

        valid_exams = []
        for i, e in enumerate(exams):
            voto_raw = e[2]
            if voto_raw is None:
                continue

            voto_str = str(voto_raw).strip().upper()
            if voto_str.endswith("L") and voto_str[:-1].isdigit():
                voto = int(voto_str[:-1])
                valid_exams.append((i + 1, voto))
            elif voto_str.isdigit():
                voto = int(voto_str)
                valid_exams.append((i + 1, voto))

        if not exams:
            ctk.CTkLabel(
                self.exam_chart_frame, text="Nessun esame inserito!", font=("Arial", 16)
            ).pack(pady=20)
            return
        if not valid_exams:
            ctk.CTkLabel(
                self.exam_chart_frame,
                text="Nessun voto numerico disponibile per il grafico!",
                font=("Arial", 16),
            ).pack(pady=20)
            return

        exam_indices, exam_scores = zip(*valid_exams)
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(exam_indices, exam_scores, marker="o", color="#e63946", linewidth=2)
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

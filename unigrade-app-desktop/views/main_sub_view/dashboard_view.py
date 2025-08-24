import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from controllers.student_controller import get_student
from controllers.exam_controller import get_exams
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils import resource_path
from PIL import Image, ImageTk, ImageDraw


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.student_id = student_id
        self.avatar_path = None

        # Recupera dati studente
        self.student = get_student(student_id) or {
            "nome": "N/D",
            "cognome": "N/D",
            "matricola": "N/D",
            "corso": "N/D",
        }

        # --- Canvas scrollabile ---
        self.canvas = tk.Canvas(self, bg="#1c1c1c", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#1c1c1c")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.bind_mousewheel()

        # --- Layout griglia principale ---
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)

        # --- Frame centrale per tutti i contenuti ---
        self.center_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.center_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
        self.center_frame.grid_columnconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(1, weight=2)
        self.center_frame.grid_rowconfigure(0, weight=1)
        self.center_frame.grid_rowconfigure(1, weight=1)

        # --- Inizializza componenti ---
        self.init_avatar()
        self.init_student_info()
        self.init_refresh_button()
        self.init_exam_chart()

        # --- Posizionamento centrato ---
        self.avatar_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.info_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.refresh_btn.grid(row=0, column=2, sticky="ne", padx=20, pady=20)
        self.exam_chart_frame.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=20, pady=30
        )

    # ------------------------
    # BIND ROTELLINA
    # ------------------------
    def bind_mousewheel(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind_all(
            "<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units")
        )
        self.canvas.bind_all(
            "<Button-5>", lambda e: self.canvas.yview_scroll(1, "units")
        )

    def init_avatar(self):
        avatar_frame = ctk.CTkFrame(
            self.center_frame, corner_radius=20, fg_color="#2a2a2a"
        )
        avatar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=20)
        avatar_frame.grid_columnconfigure(0, weight=1)

        self.avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="Icona Avatar - Avatar",
            font=("Arial", 16, "bold"),
            text_color="#4da6ff",  # colore del testo
            fg_color="#1c1c1c",  # colore di sfondo della label
            corner_radius=10,  # bordi arrotondati
            padx=10,
            pady=5,  # padding interno
        )
        self.avatar_label.grid(row=0, column=0, pady=(15, 10))

        # Contenitore immagine avatar
        self.avatar_img_label = ctk.CTkLabel(
            avatar_frame,
            text="(clicca per caricare foto)",
            width=180,
            height=180,
            fg_color="#444",
            corner_radius=90,
        )
        self.avatar_img_label.grid(row=1, column=0, pady=10)
        self.avatar_img_label.bind("<Button-1>", self.upload_avatar)

    def display_avatar(self, path):
        # Carica immagine
        img = Image.open(path)

        # Ridimensiona mantenendo proporzioni e inserisci in cerchio
        max_size = 180
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        # Crea mask circolare
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)

        # Applica mask
        img_circle = Image.new("RGBA", img.size)
        img_circle.paste(img, (0, 0), mask=mask)

        # Converti in PhotoImage per Tkinter
        self.avatar_img = ImageTk.PhotoImage(img_circle)
        self.avatar_img_label.configure(image=self.avatar_img, text="")

    def upload_avatar(self, event):
        file_path = filedialog.askopenfilename(
            title="Seleziona immagine",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")],
        )
        if file_path:
            self.avatar_path = file_path
            self.display_avatar(file_path)

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

        # Nome e corso
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
        exams_with_vote = [e for e in exams if e[2] is not None]
        totale_cfu = sum([e[3] for e in exams_with_vote]) if exams_with_vote else 0
        totale_cfu_possibile = sum([e[3] for e in exams]) if exams else 0
        media = (
            sum([e[2] * e[3] for e in exams_with_vote]) / totale_cfu
            if totale_cfu > 0
            else 0
        )

        summary_frame = ctk.CTkFrame(self.info_frame, corner_radius=10, fg_color="#333")
        summary_frame.pack(fill="x", padx=20, pady=(15, 25))

        ctk.CTkLabel(
            summary_frame,
            text=f"📚 Esami completati: {len(exams_with_vote)}",
            font=("Arial", 16),
        ).pack(pady=5)
        ctk.CTkLabel(
            summary_frame,
            text=(
                f"🎯 Media ponderata: {media:.2f}"
                if exams_with_vote
                else "🎯 Media ponderata: N/A"
            ),
            font=("Arial", 16),
        ).pack(pady=5)
        ctk.CTkLabel(
            summary_frame,
            text=f"💎 CFU totali: {totale_cfu}/{totale_cfu_possibile}",
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
        self.refreshing = False

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

    # ------------------------
    # ANIMAZIONE ROTAZIONE ICONA
    # ------------------------
    def animate_refresh(self, angle=0):
        if not self.refreshing:
            return
        rotated = self.refresh_img_orig.rotate(angle)
        self.refresh_photo = ImageTk.PhotoImage(rotated)
        self.refresh_btn.configure(image=self.refresh_photo)
        self.after(50, lambda: self.animate_refresh(angle + 15))

    # ------------------------
    # REFRESH DASHBOARD
    # ------------------------
    def refresh_content(self):
        if self.refreshing:
            return
        self.refreshing = True
        self.animate_refresh()
        for w in self.center_frame.winfo_children():
            w.destroy()
        self.init_avatar()
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
        if not exams:
            ctk.CTkLabel(
                self.exam_chart_frame, text="Nessun esame inserito!", font=("Arial", 16)
            ).pack(pady=20)
            return

        valid_exams = [(i + 1, e[2]) for i, e in enumerate(exams) if e[2] is not None]
        if not valid_exams:
            ctk.CTkLabel(
                self.exam_chart_frame,
                text="Nessun voto disponibile per il grafico!",
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

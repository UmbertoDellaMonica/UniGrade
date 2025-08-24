import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from controllers.student_controller import get_student
from controllers.exam_controller import get_exams
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.student_id = student_id
        self.avatar_path = None  # Path locale dell'avatar

        # Recupera dati studente
        self.student = get_student(student_id)
        if not self.student:
            self.student = {
                "nome": "N/D",
                "cognome": "N/D",
                "matricola": "N/D",
                "corso": "N/D",
            }

        # --- Canvas principale scrollabile ---
        self.canvas = tk.Canvas(self, bg="#1c1c1c", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#1c1c1c")

        # Aggiorna area scrollabile
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 🔥 Binding rotellina
        self.bind_mousewheel()

        # Layout principale: 3 colonne
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=2)
        self.scrollable_frame.grid_columnconfigure(2, weight=3)

        # --- Avatar ---
        self.init_avatar()

        # --- Card info studente ---
        self.init_student_info()

        # --- Grafico esami ---
        self.init_exam_chart()

    # ------------------------
    # Gestione rotellina
    # ------------------------
    def bind_mousewheel(self):
        def _on_mousewheel(event):
            # Windows / Linux
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_mousewheel_mac(event, direction):
            # macOS
            self.canvas.yview_scroll(direction, "units")

        # Windows e Linux
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # macOS
        self.canvas.bind_all("<Button-4>", lambda e: _on_mousewheel_mac(e, -1))
        self.canvas.bind_all("<Button-5>", lambda e: _on_mousewheel_mac(e, 1))

    # ------------------------
    # AVATAR
    # ------------------------
    def init_avatar(self):
        avatar_frame = ctk.CTkFrame(
            self.scrollable_frame, corner_radius=20, fg_color="#2a2a2a"
        )
        avatar_frame.grid(row=0, column=0, sticky="n", padx=(10, 20), pady=20)
        avatar_frame.grid_rowconfigure(0, weight=1)
        avatar_frame.grid_columnconfigure(0, weight=1)

        self.avatar_label = ctk.CTkLabel(
            avatar_frame, text="Avatar", font=("Arial", 18, "bold")
        )
        self.avatar_label.pack(pady=(20, 10))

        self.avatar_img_label = ctk.CTkLabel(
            avatar_frame,
            text="(clicca per caricare foto)",
            width=150,
            height=150,
            fg_color="#444",
            corner_radius=75,
        )
        self.avatar_img_label.pack(pady=10)
        self.avatar_img_label.bind("<Button-1>", self.upload_avatar)

    def upload_avatar(self, event):
        file_path = filedialog.askopenfilename(
            title="Seleziona immagine",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")],
        )
        if file_path:
            self.avatar_path = file_path
            self.display_avatar(file_path)

    def display_avatar(self, path):
        img = Image.open(path).resize((150, 150))
        self.avatar_img = ImageTk.PhotoImage(img)
        self.avatar_img_label.configure(image=self.avatar_img, text="")

    # ------------------------
    # CARD INFO STUDENTE
    # ------------------------
    def init_student_info(self):
        info_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=20,
            fg_color="#2a2a2a",
            border_width=2,
            border_color="#4da6ff",
        )
        info_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=20)
        info_frame.grid_rowconfigure(0, weight=1)
        info_frame.grid_columnconfigure(0, weight=1)

        # Nome e corso
        nome_completo = f"{self.student['nome']} {self.student['cognome']}"
        ctk.CTkLabel(info_frame, text=nome_completo, font=("Arial", 24, "bold")).pack(
            pady=(20, 5)
        )
        ctk.CTkLabel(
            info_frame,
            text=f"{self.student['corso']}",
            font=("Arial", 16, "italic"),
            text_color="#4da6ff",
        ).pack(pady=(0, 15))

        # Divider
        divider = ctk.CTkFrame(info_frame, fg_color="#444", height=2)
        divider.pack(fill="x", padx=20, pady=10)

        # Matricola
        matricola_frame = ctk.CTkFrame(info_frame, corner_radius=10, fg_color="#333")
        matricola_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(
            matricola_frame,
            text=f"🆔 Matricola: {self.student['matricola']}",
            font=("Arial", 14, "bold"),
        ).pack(padx=10, pady=5)

        # Riassunto esami
        exams = get_exams(self.student_id)
        totale_cfu = sum([e[3] for e in exams]) if exams else 0
        media = sum([e[2] * e[3] for e in exams]) / totale_cfu if exams else 0

        summary_frame = ctk.CTkFrame(info_frame, corner_radius=10, fg_color="#333")
        summary_frame.pack(fill="x", padx=20, pady=(10, 20))

        ctk.CTkLabel(
            summary_frame, text=f"📚 Esami completati: {len(exams)}", font=("Arial", 14)
        ).pack(pady=5)
        ctk.CTkLabel(
            summary_frame,
            text=(
                f"🎯 Media ponderata: {media:.2f}"
                if exams
                else "🎯 Media ponderata: N/A"
            ),
            font=("Arial", 14),
        ).pack(pady=5)
        ctk.CTkLabel(
            summary_frame, text=f"💎 CFU totali: {totale_cfu}", font=("Arial", 14)
        ).pack(pady=5)

    # ------------------------
    # GRAFICO ANDAMENTO VOTI
    # ------------------------
    def init_exam_chart(self):
        exams_frame = ctk.CTkFrame(
            self.scrollable_frame, corner_radius=15, fg_color="#2a2a2a"
        )
        exams_frame.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=(20, 10)
        )

        exams = get_exams(self.student_id)
        if not exams:
            ctk.CTkLabel(
                exams_frame,
                text="Nessun esame inserito!",
                font=("Arial", 16),
                fg_color="#2a2a2a",
            ).pack(pady=20)
            return

        exam_scores = [e[2] for e in exams]

        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(
            range(1, len(exam_scores) + 1),
            exam_scores,
            marker="o",
            color="#e63946",
            linewidth=2,
        )
        ax.set_ylim(18, 31)
        ax.set_title("Andamento voti", color="white")
        ax.set_xlabel("Esami", color="white")
        ax.set_ylabel("Voto", color="white")
        ax.set_xticks(range(1, len(exam_scores) + 1))
        ax.set_xticklabels(
            range(1, len(exam_scores) + 1),
            rotation=45,
            ha="right",
            fontsize=10,
            color="white",
        )
        ax.tick_params(axis="y", colors="white", labelsize=10)
        ax.set_facecolor("#2a2a2a")
        fig.patch.set_facecolor("#1c1c1c")

        canvas_fig = FigureCanvasTkAgg(fig, master=exams_frame)
        canvas_fig.draw()
        canvas_fig.get_tk_widget().pack(fill="both", expand=True, pady=20, padx=10)

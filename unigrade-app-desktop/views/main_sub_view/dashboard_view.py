import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from controllers.student_controller import get_student
from controllers.exam_controller import get_exams
from matplotlib.figure import Figure
from utils import resource_path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk


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

        # --- Pulsante refresh piccolo ---
        self.init_refresh_button()

        # --- Grafico esami ---
        self.init_exam_chart()

    # ------------------------
    # BIND ROTELLINA
    # ------------------------
    def bind_mousewheel(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_mousewheel_mac(event, direction):
            self.canvas.yview_scroll(direction, "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
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
    # INFO STUDENT
    # ------------------------
    def init_student_info(self):
        self.info_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=20,
            fg_color="#2a2a2a",
            border_width=2,
            border_color="#4da6ff",
        )
        self.info_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=20)
        self.info_frame.grid_rowconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(0, weight=1)

        # Nome e corso
        nome_completo = f"{self.student['nome']} {self.student['cognome']}"
        ctk.CTkLabel(
            self.info_frame, text=nome_completo, font=("Arial", 24, "bold")
        ).pack(pady=(20, 5))
        ctk.CTkLabel(
            self.info_frame,
            text=f"{self.student['corso']}",
            font=("Arial", 16, "italic"),
            text_color="#4da6ff",
        ).pack(pady=(0, 15))

        # Divider
        divider = ctk.CTkFrame(self.info_frame, fg_color="#444", height=2)
        divider.pack(fill="x", padx=20, pady=10)

        # Matricola
        matricola_frame = ctk.CTkFrame(
            self.info_frame, corner_radius=10, fg_color="#333"
        )
        matricola_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(
            matricola_frame,
            text=f"🆔 Matricola: {self.student['matricola']}",
            font=("Arial", 14, "bold"),
        ).pack(padx=10, pady=5)

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
        summary_frame.pack(fill="x", padx=20, pady=(10, 20))

        ctk.CTkLabel(
            summary_frame,
            text=f"📚 Esami completati: {len(exams_with_vote)}",
            font=("Arial", 14),
        ).pack(pady=5)
        ctk.CTkLabel(
            summary_frame,
            text=(
                f"🎯 Media ponderata: {media:.2f}"
                if exams_with_vote
                else "🎯 Media ponderata: N/A"
            ),
            font=("Arial", 14),
        ).pack(pady=5)
        ctk.CTkLabel(
            summary_frame,
            text=f"💎 CFU totali: {totale_cfu}/{totale_cfu_possibile}",
            font=("Arial", 14),
        ).pack(pady=5)

    # ------------------------
    # REFRESH BUTTON PICCOLO
    # ------------------------
    def init_refresh_button(self):
        # Frame piccolo in alto a destra della card info studente
        self.refresh_frame = ctk.CTkFrame(
            self.scrollable_frame, corner_radius=10, fg_color="transparent"
        )
        self.refresh_frame.grid(row=0, column=2, sticky="ne", padx=10, pady=10)

        # Icona refresh
        self.refresh_img_orig = Image.open(
            resource_path("assets/icons/reload.png")
        ).resize((20, 20))
        self.refresh_photo = ImageTk.PhotoImage(self.refresh_img_orig)

        self.refreshing = False

        self.refresh_btn = ctk.CTkButton(
            self.refresh_frame,
            image=self.refresh_photo,
            text="",
            width=30,
            height=30,
            fg_color="#444444",  # grigio scuro
            hover_color="#666666",  # leggermente più chiaro al passaggio del mouse
            corner_radius=15,
            command=self.refresh_content,
        )
        self.refresh_btn.pack()

        # Tooltip
        self.tooltip = ctk.CTkLabel(
            self.refresh_frame,
            text="Aggiorna dashboard",
            font=("Arial", 10),
            fg_color="#444",
            text_color="white",
            corner_radius=5,
            padx=5,
            pady=2,
        )
        self.tooltip.place_forget()

        # Funzioni per mostrare/nascondere tooltip sotto il pulsante
        def show_tooltip(event):
            x = (
                self.refresh_btn.winfo_x()
                + self.refresh_btn.winfo_width() // 2
                - self.tooltip.winfo_reqwidth() // 2
            )
            y = self.refresh_btn.winfo_y() + self.refresh_btn.winfo_height() + 5
            self.tooltip.place(x=x, y=y)

        def hide_tooltip(event):
            self.tooltip.place_forget()

        self.refresh_btn.bind("<Enter>", show_tooltip)
        self.refresh_btn.bind("<Leave>", hide_tooltip)

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
        # Ricarica tutto il contenuto della dashboard
        for w in self.scrollable_frame.winfo_children():
            w.destroy()
        self.init_avatar()
        self.init_student_info()
        self.init_refresh_button()
        self.init_exam_chart()
        # Ferma animazione dopo 1 secondo
        self.after(1000, lambda: setattr(self, "refreshing", False))

    # ------------------------
    # CHART INFO STUDENTE
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

        valid_exams = [(i + 1, e[2]) for i, e in enumerate(exams) if e[2] is not None]

        if not valid_exams:
            ctk.CTkLabel(
                exams_frame,
                text="Nessun voto disponibile per il grafico!",
                font=("Arial", 16),
                fg_color="#2a2a2a",
            ).pack(pady=20)
            return

        exam_indices, exam_scores = zip(*valid_exams)

        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(
            exam_indices,
            exam_scores,
            marker="o",
            color="#e63946",
            linewidth=2,
        )
        ax.set_ylim(18, 31)
        ax.set_title("Andamento voti", color="white")
        ax.set_xlabel("Esami", color="white")
        ax.set_ylabel("Voto", color="white")
        ax.set_xticks(exam_indices)
        ax.set_xticklabels(
            exam_indices,
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

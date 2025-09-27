import customtkinter as ctk
from controllers.exam_controller import get_exams
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplcursors


class ExamChartComponent(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master, corner_radius=15, fg_color="#2a2a2a")
        self.pack(fill="both", padx=20, pady=80, expand=True)
        self.student_id = student_id
        self._create_chart()

    def _create_chart(self):
        exams = get_exams(self.student_id)
        valid_exams, exam_labels = [], []

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
            acr = (
                "".join(word[0].upper() for word in nome_raw.split())
                if len(nome_raw) > 15
                else nome_raw
            )
            exam_labels.append((acr, nome_raw))

        if not valid_exams:
            text = (
                "Nessun esame inserito!"
                if not exams
                else "Nessun voto numerico disponibile!"
            )
            ctk.CTkLabel(self, text=text, font=("Arial", 16), text_color="white").pack(
                pady=20
            )
            return

        indices, scores = zip(*valid_exams)
        fig = plt.Figure(figsize=(14, 10), dpi=100)
        ax = fig.add_subplot(111)

        colors = [
            "#e63946" if v < 24 else "#f1c40f" if v < 28 else "#2ecc71" for v in scores
        ]
        ax.scatter(indices, scores, color=colors, s=140)
        ax.plot(indices, scores, color="#e63946", linewidth=2, alpha=0.6)

        ax.set_ylim(18, 31)
        ax.set_title("Andamento voti", color="white")
        ax.set_xlabel("Esami", color="white")
        ax.set_ylabel("Voto", color="white")
        ax.set_xticks(indices)
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

        canvas_fig = FigureCanvasTkAgg(fig, master=self)
        canvas_fig.draw()
        canvas_fig.get_tk_widget().pack(fill="both", expand=True, pady=20, padx=10)

        cursor = mplcursors.cursor(ax, hover=True)
        cursor.connect(
            "add",
            lambda sel: sel.annotation.set_text(
                f"{exam_labels[int(sel.index)][1]}\nVoto: {scores[int(sel.index)]}"
            ),
        )

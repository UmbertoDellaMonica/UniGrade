import customtkinter as ctk
from controllers.exam_controller import get_exams
from configuration.unigrade_configuration import DISPLAY_30L, PASSED, NOT_PASSED


class StudentInfoComponent(ctk.CTkFrame):
    def __init__(self, master, student, student_id):
        super().__init__(
            master,
            corner_radius=20,
            fg_color="#2a2a2a",
            border_width=2,
            border_color="#4da6ff",
        )
        self.student = student
        self.student_id = student_id

        # Titolo
        ctk.CTkLabel(
            self,
            text="Informazioni Studente",
            font=("Arial", 20, "bold"),
            text_color="#4da6ff",
        ).pack(pady=(15, 15))

        # Details frame
        details_frame = ctk.CTkFrame(self, fg_color="#1c1c1c", corner_radius=15)
        details_frame.pack(fill="both", padx=15, pady=(0, 15))

        for label, value in [
            ("🧑 Nome", student["nome"]),
            ("👤 Cognome", student["cognome"]),
            ("🎓 Corso", student["corso"]),
            ("🆔 Matricola", student["matricola"]),
        ]:
            ctk.CTkLabel(
                details_frame, text=f"{label}: {value}", font=("Arial", 14)
            ).pack(anchor="w", pady=5, padx=10)

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
            if voto_str == NOT_PASSED:
                count_non_superati += 1
                continue
            if voto_str == PASSED:
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

        for label, val in stats:
            ctk.CTkLabel(
                parent_frame,
                text=f"{label}: {val}",
                font=("Arial", 14),
                anchor="w",
                padx=10,
            ).pack(fill="x", pady=5)

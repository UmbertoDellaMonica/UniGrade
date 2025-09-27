import customtkinter as ctk
from configuration.unigrade_configuration import DISPLAY_30L, PASSED, NOT_PASSED


class AddExamDialog(ctk.CTkToplevel):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.result = None
        self.student_id = student_id
        self.title("Aggiungi Nuovo Esame")
        self.geometry("400x400")
        self.grab_set()
        self.resizable(False, False)

        # Titolo
        ctk.CTkLabel(self, text="📚 Nuovo Esame", font=("Arial", 18, "bold")).pack(
            pady=(20, 10)
        )

        # Frame campi
        fields_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#2e2e3e")
        fields_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Nome esame
        ctk.CTkLabel(fields_frame, text="Nome Esame", font=("Arial", 14)).grid(
            row=0, column=0, sticky="e", padx=10, pady=10
        )
        self.exam_name = ctk.CTkEntry(fields_frame, width=200)
        self.exam_name.grid(row=0, column=1, padx=10, pady=10)

        # Voto
        ctk.CTkLabel(fields_frame, text="Voto", font=("Arial", 14)).grid(
            row=1, column=0, sticky="e", padx=10, pady=10
        )
        voti_possibili = (
            ["", PASSED, NOT_PASSED] + [str(i) for i in range(18, 31)] + [DISPLAY_30L]
        )
        self.vote_combo = ctk.CTkComboBox(
            fields_frame, values=voti_possibili, width=120
        )
        self.vote_combo.set("")
        self.vote_combo.grid(row=1, column=1, padx=10, pady=10)

        # CFU
        ctk.CTkLabel(fields_frame, text="CFU", font=("Arial", 14)).grid(
            row=2, column=0, sticky="e", padx=10, pady=10
        )
        self.cfu_entry = ctk.CTkEntry(fields_frame, width=100)
        self.cfu_entry.grid(row=2, column=1, padx=10, pady=10)

        # Label messaggi errore
        self.msg_label = ctk.CTkLabel(
            self, text="", font=("Arial", 12), text_color="#ff6666"
        )
        self.msg_label.pack(pady=(5, 0))

        # Pulsanti
        ctk.CTkButton(
            self,
            text="Aggiungi",
            command=self._on_submit,
            width=180,
            fg_color="#4da6ff",
            hover_color="#66b3ff",
        ).pack(pady=(20, 5))
        ctk.CTkButton(
            self,
            text="Annulla",
            command=self.destroy,
            width=180,
            fg_color="#888888",
            hover_color="#aaaaaa",
        ).pack(pady=(0, 15))

    def _on_submit(self):
        nome = self.exam_name.get().strip()
        voto_text = self.vote_combo.get().strip()
        cfu_text = self.cfu_entry.get().strip()

        if not nome:
            self.msg_label.configure(text="Inserisci il nome dell'esame!")
            return

        try:
            cfu = int(cfu_text)
            if cfu <= 0:
                self.msg_label.configure(text="CFU deve essere un numero positivo!")
                return
        except ValueError:
            self.msg_label.configure(text="CFU deve essere un numero valido!")
            return

        voto_up = voto_text.upper()
        if voto_up in [PASSED, NOT_PASSED, DISPLAY_30L]:
            voto = voto_up
        elif voto_text == "":
            voto = None
        else:
            try:
                vn = int(voto_text)
                if vn < 18 or vn > 30:
                    self.msg_label.configure(
                        text="Voto numerico deve essere tra 18 e 30 o 30L!"
                    )
                    return
                voto = vn
            except ValueError:
                self.msg_label.configure(text="Voto non valido!")
                return

        # Stato calcolato automaticamente
        if voto is None or voto == "":
            stato = "In attesa ⏳"
        elif voto in [PASSED, NOT_PASSED]:
            stato = voto + (" ✅" if voto == PASSED else " ❌")
        elif voto == DISPLAY_30L or (isinstance(voto, int) and 18 <= voto <= 30):
            stato = "Passato ✅"
        else:
            stato = "Non superato ❌"

        self.result = {"nome": nome, "voto": voto, "cfu": cfu}
        self.destroy()

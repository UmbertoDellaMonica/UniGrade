import customtkinter as ctk


class ActionsBar(ctk.CTkFrame):
    def __init__(self, master, exams_table):
        super().__init__(master, fg_color="#2e2e3e", corner_radius=10)
        self.exams_table = exams_table

        add_btn = ctk.CTkButton(
            self, text="➕ Aggiungi Esame", command=self.exams_table.add_exam
        )
        add_btn.pack(side="left", padx=10, pady=5)

        edit_btn = ctk.CTkButton(
            self, text="✏️ Modifica", command=self.exams_table.edit_exam
        )
        edit_btn.pack(side="left", padx=10, pady=5)

        remove_btn = ctk.CTkButton(
            self, text="🗑️ Rimuovi", command=self.exams_table.remove_exam
        )
        remove_btn.pack(side="left", padx=10, pady=5)

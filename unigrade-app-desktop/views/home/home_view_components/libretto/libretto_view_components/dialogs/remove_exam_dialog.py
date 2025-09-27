import customtkinter as ctk


class RemoveExamDialog(ctk.CTkToplevel):
    def __init__(self, master, student_id, values):
        super().__init__(master)
        self.confirmed = False
        self.title("Rimuovi Esame")
        self.geometry("300x150")
        self.grab_set()

        label = ctk.CTkLabel(self, text=f"Vuoi rimuovere l'esame '{values[0]}'?")
        label.pack(pady=20)

        confirm_btn = ctk.CTkButton(
            self, text="Conferma", fg_color="red", command=self._on_confirm
        )
        confirm_btn.pack(side="left", padx=30, pady=10)

        cancel_btn = ctk.CTkButton(self, text="Annulla", command=self.destroy)
        cancel_btn.pack(side="right", padx=30, pady=10)

    def _on_confirm(self):
        self.confirmed = True
        self.destroy()

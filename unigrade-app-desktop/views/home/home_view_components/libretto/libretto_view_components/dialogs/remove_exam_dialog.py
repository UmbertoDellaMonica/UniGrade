import customtkinter as ctk


class RemoveExamDialog(ctk.CTkToplevel):
    def __init__(self, master, student_id, values):
        super().__init__(master)
        self.confirmed = False
        self.title("Rimuovi Esame")
        self.geometry("300x150")
        self.grab_set()

        # Label
        label = ctk.CTkLabel(self, text=f"Vuoi rimuovere l'esame '{values[0]}'?")
        label.pack(pady=20)

        # Frame per i pulsanti
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10, fill="x")

        # Pulsante Conferma
        confirm_btn = ctk.CTkButton(
            button_frame, text="Conferma", fg_color="red", command=self._on_confirm
        )
        confirm_btn.pack(side="left", expand=True, padx=20)

        # Pulsante Annulla
        cancel_btn = ctk.CTkButton(button_frame, text="Annulla", command=self.destroy)
        cancel_btn.pack(side="right", expand=True, padx=20)

    def _on_confirm(self):
        self.confirmed = True
        self.destroy()

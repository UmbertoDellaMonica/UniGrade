import customtkinter as ctk
from PIL import Image
from configuration.unigrade_configuration import resource_path


class HeaderSection(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=15, fg_color="#2e2e3e")

        title = ctk.CTkLabel(self, text="📚 Libretto Esami", font=("Arial", 24, "bold"))
        title.pack(pady=(5, 5))

        self.icons = {
            "exam": self._load_icon("book.png"),
            "vote": self._load_icon("star.png"),
            "cfu": self._load_icon("coin.png"),
            "status": self._load_icon("check.png"),
        }

        header_frame = ctk.CTkFrame(self, fg_color="#2b2b3d", corner_radius=8)
        header_frame.pack(fill="x", pady=(5, 0))

        for text, key in [
            ("Nome Esame", "exam"),
            ("Voto", "vote"),
            ("CFU", "cfu"),
            ("Stato", "status"),
        ]:
            lbl = ctk.CTkLabel(
                header_frame,
                text=f" {text}",
                image=self.icons[key],
                compound="left",
                font=("Arial", 14, "bold"),
                padx=10,
            )
            lbl.pack(side="left", expand=True, fill="x", padx=5, pady=5)

    def _load_icon(self, filename):
        return ctk.CTkImage(
            light_image=Image.open(resource_path(f"assets/icons/{filename}")),
            dark_image=Image.open(resource_path(f"assets/icons/{filename}")),
            size=(20, 20),
        )

import customtkinter as ctk
import tkinter as tk
from views.home.home_view_components.libretto.libretto_view_components.libretto_header_component import (
    HeaderSection,
)
from views.home.home_view_components.libretto.libretto_view_components.libretto_exam_table_component import (
    ExamsTable,
)
from views.home.home_view_components.libretto.libretto_view_components.libretto_action_bar_component import (
    ActionsBar,
)


class LibrettoView(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.master = master
        self.student_id = student_id
        self.pack(fill="both", expand=True)

        # --- canvas scrollabile ---
        self.canvas = tk.Canvas(self, bg="#1c1c1c", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#1c1c1c")
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind("<Configure>", self._resize_scrollable_frame)

        # --- sezioni ---
        self.header = HeaderSection(self.scrollable_frame)
        self.header.pack(fill="x", pady=(10, 0))

        self.exams_table = ExamsTable(self.scrollable_frame, student_id)
        self.exams_table.pack(fill="both", expand=True, padx=20, pady=(10, 0))

        self.actions = ActionsBar(self.scrollable_frame, self.exams_table)
        self.actions.pack(pady=30, padx=20, fill="x")

        # scroll all’inizio
        self.scrollable_frame.update_idletasks()
        self.canvas.yview_moveto(0)

    def _resize_scrollable_frame(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

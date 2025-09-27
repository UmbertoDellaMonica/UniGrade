import customtkinter as ctk
from views.home.home_view_components.dashboard.dashboard_view_components.dashboard_scrollable_frame_component import (
    ScrollableFrame,
)
from views.home.home_view_components.dashboard.dashboard_view_components.dashboard_header_component import (
    DashboardHeader,
)
from views.home.home_view_components.dashboard.dashboard_view_components.dashboard_exam_chart_component import (
    ExamChartComponent,
)
from controllers.student_controller import get_student


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.student_id = student_id
        self.student = get_student(student_id) or {
            "nome": "N/D",
            "cognome": "N/D",
            "corso": "N/D",
            "matricola": "N/D",
            "avatar_path": None,
        }

        self.scrollable_frame = ScrollableFrame(self)
        self.header = DashboardHeader(
            self.scrollable_frame.scrollable_frame,
            self.student,
            self.student_id,
            self._refresh,
        )
        self.exam_chart = ExamChartComponent(
            self.scrollable_frame.scrollable_frame, self.student_id
        )

    def _refresh(self):
        self.destroy()
        DashboardView(self.master, self.student_id)

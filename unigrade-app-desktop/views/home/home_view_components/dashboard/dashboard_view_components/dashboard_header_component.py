import customtkinter as ctk
from views.home.home_view_components.dashboard.dashboard_view_components.dashboard_avatar_component import (
    AvatarComponent,
)

from views.home.home_view_components.dashboard.dashboard_view_components.dashboard_student_info_component import (
    StudentInfoComponent,
)
from PIL import Image
from configuration.unigrade_configuration import resource_path


class DashboardHeader(ctk.CTkFrame):
    def __init__(self, master, student, student_id, refresh_callback):
        super().__init__(master, fg_color="#1c1c1c")
        self.pack(fill="x", padx=20, pady=0)

        # Avatar
        avatar_path = (
            student["avatar_path"]
            if student is not None and "avatar_path" in student.keys()
            else None
        )
        self.avatar_component = AvatarComponent(
            self, student_id, avatar_path=avatar_path
        )
        self.avatar_component.avatar_frame.pack(side="left", padx=(0, 20), anchor="n")

        # Info studente

        self.info_frame = StudentInfoComponent(self, student, student_id)
        self.info_frame.pack(
            side="left", fill="both", expand=True, padx=(0, 20), pady=0, anchor="n"
        )

        # Refresh button

        self.refresh_ctk_image = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/icons/reload.png")),
            dark_image=Image.open(resource_path("assets/icons/reload.png")),
            size=(28, 28),
        )

        self.refresh_btn = ctk.CTkButton(
            self,
            image=self.refresh_ctk_image,
            text="",
            width=50,
            height=50,
            fg_color="#4da6ff",
            hover_color="#6ab0ff",
            corner_radius=25,
            command=refresh_callback,
        )
        self.refresh_btn.pack(side="right", padx=10, pady=0, anchor="n")

import customtkinter as ctk
from PIL import Image, ImageDraw
from customtkinter import CTkImage
from tkinter import filedialog
from controllers.student_controller import update_student_avatar


class AvatarComponent:
    """Avatar studente semplice, compatibile con pack"""

    def __init__(self, parent_frame, student_id, avatar_path=None):
        self.parent_frame = parent_frame
        self.student_id = student_id
        self.avatar_path = avatar_path
        self.avatar_img = None

        self.init_avatar_frame()
        if self.avatar_path:
            self.display_avatar(self.avatar_path)

    def init_avatar_frame(self):
        # Frame principale dell'avatar
        self.avatar_frame = ctk.CTkFrame(
            self.parent_frame,
            corner_radius=20,
            fg_color="#2a2a2a",
            border_width=2,
            border_color="#444",
        )
        self.avatar_frame.pack(fill="x", padx=20, pady=20)

        # Label titolo
        self.avatar_label = ctk.CTkLabel(
            self.avatar_frame,
            text="Avatar Studente",
            font=("Arial", 16, "bold"),
            text_color="#4da6ff",
            fg_color="#1c1c1c",
            pady=5,
            padx=10,
            corner_radius=10,
        )
        self.avatar_label.pack(pady=(10, 10))

        # Label immagine
        self.avatar_img_label = ctk.CTkLabel(
            self.avatar_frame,
            text="➕ Clicca per caricare",
            width=180,
            height=180,
            fg_color="#444",
            corner_radius=90,
            text_color="#aaa",
            font=("Arial", 14, "italic"),
        )
        self.avatar_img_label.pack(pady=10)
        self.avatar_img_label.bind("<Button-1>", self.upload_avatar)
        self.avatar_img_label.bind("<Enter>", self.on_hover)
        self.avatar_img_label.bind("<Leave>", self.on_leave)

    def display_avatar(self, path):
        img = Image.open(path)
        max_size = 180
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        # Maschera circolare
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)

        img_circle = Image.new("RGBA", img.size)
        img_circle.paste(img, (0, 0), mask=mask)

        self.avatar_img = CTkImage(
            light_image=img_circle, dark_image=img_circle, size=(180, 180)
        )
        self.avatar_img_label.configure(image=self.avatar_img, text="")

        self.avatar_frame.configure(border_color="#4da6ff")

    def upload_avatar(self, event=None):
        file_path = filedialog.askopenfilename(
            title="Seleziona immagine",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")],
        )
        if not file_path:
            return

        self.avatar_path = file_path
        self.display_avatar(file_path)
        update_student_avatar(self.student_id, file_path)
        self.animate_click()

    def on_hover(self, event):
        self.avatar_img_label.configure(fg_color="#4da6ff", text_color="#fff")

    def on_leave(self, event):
        if self.avatar_img:
            self.avatar_img_label.configure(fg_color="#2a2a2a", text_color="#fff")
        else:
            self.avatar_img_label.configure(fg_color="#444", text_color="#aaa")

    def animate_click(self):
        def shrink():
            self.avatar_img_label.configure(width=160, height=160)
            self.parent_frame.after(100, expand)

        def expand():
            self.avatar_img_label.configure(width=180, height=180)

        shrink()

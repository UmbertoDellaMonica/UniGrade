import customtkinter as ctk
from configuration.unigrade_configuration import show_temp_message


from views.register.service.register_view_service import RegisterService


from views.register.register_view_components.register_course_dropdown_component import (
    CourseDropdown,
)
from views.register.register_view_components.register_form_entry_component import (
    FormEntry,
)
from views.register.register_view_components.register_title_component import (
    RegisterTitle,
)


class RegisterView:
    def __init__(self, master, previous_view=None):
        self.master = master
        self.previous_view = previous_view

        # Frame principale
        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Titolo
        self.title = RegisterTitle(self.frame)
        self.title.grid_configure(pady=(20, 40))  # più spazio sotto il titolo

        # Form base
        labels = ["Nome", "Cognome", "Matricola", "Password", "Facoltà"]
        self.form = FormEntry(self.frame, labels)
        self.form.grid(row=1, column=0, columnspan=2, pady=(0, 20))  # spazio sotto form

        # Dropdown corso
        self.course_dropdown = CourseDropdown(self.frame)
        self.course_dropdown.grid(
            row=2, column=0, columnspan=2, pady=(0, 20)
        )  # spazio sotto dropdown

        # Colore del frame principale (per integrare i pulsanti)

        # Bottone Conferma a sinistra
        self.confirm_button = ctk.CTkButton(
            self.frame,
            text="Conferma",
            command=self.do_register,
            width=180,
            fg_color="#1f6aa5",  # integrato nel frame
        )
        self.confirm_button.grid(
            row=3, column=0, sticky="w", padx=(20, 10), pady=(30, 20)
        )

        # Bottone Indietro a destra
        self.back_button = ctk.CTkButton(
            self.frame,
            text="Indietro",
            command=self.go_back,
            width=180,
            fg_color="#888888",  # integrato nel frame
        )
        self.back_button.grid(row=3, column=1, sticky="e", padx=(10, 20), pady=(30, 20))

        # Configura colonne per distribuire lo spazio
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

    def do_register(self):
        # Validazione campi tramite service
        valid, message = RegisterService.validate_fields(self.form.entries)
        if not valid:
            show_temp_message(self.frame, message, color="red")
            return

        # Registrazione tramite service
        success, message = RegisterService.register_user(
            nome=self.form.entries["Nome"].get().strip(),
            cognome=self.form.entries["Cognome"].get().strip(),
            corso_facolta=self.course_dropdown.var.get().strip()
            + " "
            + self.form.entries["Facoltà"].get().strip(),
            matricola=self.form.entries["Matricola"].get().strip(),
            password=self.form.entries["Password"].get().strip(),
        )

        # Mostra messaggio di esito
        show_temp_message(self.frame, message, color="green" if success else "red")
        if success:
            self.master.after(1500, self.go_back)

    def go_back(self):
        self.frame.destroy()
        if self.previous_view:
            self.previous_view()
        else:
            from app import HomePage

            HomePage(self.master)

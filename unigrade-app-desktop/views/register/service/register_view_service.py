from controllers.auth_controller import register


class RegisterService:
    """Gestisce le azioni relative all'autenticazione e registrazione."""

    @staticmethod
    def validate_fields(fields: dict) -> tuple[bool, str]:
        """
        Controlla che tutti i campi non siano vuoti.
        :param fields: dict con label -> widget CTkEntry
        :return: (True, "") se tutto ok, altrimenti (False, messaggio di errore)
        """
        for lbl, widget in fields.items():
            if not widget.get().strip():
                return False, f"⚠️ Il campo '{lbl}' non può essere vuoto!"
        return True, ""

    @staticmethod
    def register_user(
        nome, cognome, corso_facolta, matricola, password
    ) -> tuple[bool, str]:
        """
        Esegue la registrazione dell'utente tramite il controller.
        :return: (True, messaggio) se registrazione avvenuta, (False, messaggio) altrimenti
        """
        success = register(nome, cognome, corso_facolta, matricola, password)
        if success:
            return True, "✅ Registrazione completata!"
        else:
            return False, "❌ Matricola già registrata!"

class Controller:
    def __init__(self, validator, database, user_interface, external_service):
        self.validator = validator
        self.database = database
        self.user_interface = user_interface
        self.external_service = external_service

    def process_registration(self):
        login, password, confirm = self.user_interface.get_registration_data()

        saved = self.database.get(login, password, confirm)

        if saved is None:
            result, error_message = self.validator.validate(login, password, confirm)
            self.database.add(login, password, confirm, result, error_message)
        else:
            result, error_message = saved

        message = f"Результат: {result}; Сообщение: {error_message}"
        self.external_service.send_result(message)

        return result, error_message
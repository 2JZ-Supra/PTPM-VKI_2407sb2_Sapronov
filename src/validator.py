from .my_project import validate_registration


class Validator:
    def validate(self, login, password, confirm):
        return validate_registration(login, password, confirm)
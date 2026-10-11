from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def get_registration_data(self):
        pass


class ConsoleUserInterface(UserInterface):
    def get_registration_data(self):
        login = input("Введите логин: ")
        password = input("Введите пароль: ")
        confirm = input("Подтвердите пароль: ")
        return login, password, confirm
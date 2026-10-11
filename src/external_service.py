from abc import ABC, abstractmethod


class ExternalService(ABC):
    @abstractmethod
    def send_result(self, message):
        pass


class EmailService(ExternalService):
    def send_result(self, message):
        print(f"Отправлено на email-сервер: {message}")
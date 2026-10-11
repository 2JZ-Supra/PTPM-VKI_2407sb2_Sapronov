import unittest
from unittest.mock import Mock, patch

from src.database import Database
from src.validator import Validator
from src.user_interface import ConsoleUserInterface, UserInterface
from src.external_service import EmailService
from src.controller import Controller


class FakeUserInterface(UserInterface):
    def __init__(self, data):
        self.data = data

    def get_registration_data(self):
        return self.data


class TestLab3(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.validator = Validator()
        self.external = Mock()

    def tearDown(self):
        self.db.close()

    # Интеграционный тест 1
    def test_integration_new_valid_registration(self):
        ui = FakeUserInterface(("user_123", "Пароль1!", "Пароль1!"))
        controller = Controller(self.validator, self.db, ui, self.external)

        result, message = controller.process_registration()

        self.assertTrue(result)
        self.assertEqual(message, "")
        self.assertEqual(
            self.db.get("user_123", "Пароль1!", "Пароль1!"),
            (True, "")
        )
        self.external.send_result.assert_called_once()
        self.assertIn("Результат: True", self.external.send_result.call_args[0][0])

    # Интеграционный тест 2
    def test_integration_new_invalid_registration(self):
        ui = FakeUserInterface(("", "Пароль1!", "Пароль1!"))
        controller = Controller(self.validator, self.db, ui, self.external)

        result, message = controller.process_registration()

        self.assertFalse(result)
        self.assertEqual(message, "Логин не может быть пустым")
        self.assertEqual(
            self.db.get("", "Пароль1!", "Пароль1!"),
            (False, "Логин не может быть пустым")
        )
        self.external.send_result.assert_called_once()

    # Интеграционный тест 3
    def test_integration_existing_record_taken_from_db(self):
        self.db.add("user_123", "Пароль1!", "Пароль1!", False, "Из БД")

        ui = FakeUserInterface(("user_123", "Пароль1!", "Пароль1!"))
        controller = Controller(self.validator, self.db, ui, self.external)

        result, message = controller.process_registration()

        self.assertFalse(result)
        self.assertEqual(message, "Из БД")
        self.external.send_result.assert_called_once()
        self.assertIn("Из БД", self.external.send_result.call_args[0][0])

    def test_database_add_get_delete(self):
        self.assertIsNone(self.db.get("user_123", "Пароль1!", "Пароль1!"))

        self.db.add("user_123", "Пароль1!", "Пароль1!", True, "")
        self.assertEqual(
            self.db.get("user_123", "Пароль1!", "Пароль1!"),
            (True, "")
        )

        self.db.delete("user_123", "Пароль1!", "Пароль1!")
        self.assertIsNone(self.db.get("user_123", "Пароль1!", "Пароль1!"))

    @patch("builtins.input", side_effect=["user_123", "Пароль1!", "Пароль1!"])
    def test_console_user_interface_uses_input(self, mock_input):
        ui = ConsoleUserInterface()
        data = ui.get_registration_data()

        self.assertEqual(data, ("user_123", "Пароль1!", "Пароль1!"))
        self.assertEqual(mock_input.call_count, 3)

    @patch("builtins.print")
    def test_email_service_sends_result(self, mock_print):
        service = EmailService()
        service.send_result("тестовое сообщение")

        mock_print.assert_called_once()
        self.assertIn("тестовое сообщение", mock_print.call_args[0][0])

    def test_validator_wrapper_calls_validation(self):
        result, message = self.validator.validate("user_123", "Пароль1!", "Пароль1!")

        self.assertTrue(result)
        self.assertEqual(message, "")


if __name__ == "__main__":
    unittest.main()
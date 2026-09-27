import unittest
from src.my_project import (
    mask_password, is_phone, is_email, is_plain_login, validate_registration
)

class TestValidationFunctions(unittest.TestCase):

    # --- Тесты для is_phone ---
    def test_is_phone_returns_true_for_valid_phone(self):
        self.assertTrue(is_phone("+7-123-456-7890"))

    def test_is_phone_returns_false_for_missing_plus(self):
        self.assertFalse(is_phone("7-123-456-7890"))

    def test_is_phone_returns_false_for_wrong_digit_count(self):
        self.assertFalse(is_phone("+7-123-45-7890"))

    def test_is_phone_returns_false_for_letters(self):
        self.assertFalse(is_phone("+7-abc-def-ghij"))

    # --- Тесты для is_email ---
    def test_is_email_returns_true_for_valid_email(self):
        self.assertTrue(is_email("user@example.com"))

    def test_is_email_returns_true_for_valid_email_with_subdomain(self):
        self.assertTrue(is_email("user.name@sub.example.co.uk"))

    def test_is_email_returns_false_for_missing_at(self):
        self.assertFalse(is_email("userexample.com"))

    def test_is_email_returns_false_for_missing_domain(self):
        self.assertFalse(is_email("user@"))

    # --- Тесты для is_plain_login ---
    def test_is_plain_login_returns_true_for_valid_login(self):
        self.assertTrue(is_plain_login("user_123"))

    def test_is_plain_login_returns_false_for_short_login(self):
        self.assertFalse(is_plain_login("usr"))

    def test_is_plain_login_returns_false_for_special_chars(self):
        self.assertFalse(is_plain_login("user!123"))

    def test_is_plain_login_returns_false_for_cyrillic(self):
        self.assertFalse(is_plain_login("пользователь"))

    # --- Тесты для mask_password ---
    def test_mask_password_returns_string_of_length_8(self):
        masked = mask_password("Password123!")
        self.assertEqual(len(masked), 8)
        self.assertIsInstance(masked, str)

    def test_mask_password_differs_for_different_passwords(self):
        self.assertNotEqual(mask_password("Password1!"), mask_password("Password2!"))

    # --- Тесты для validate_registration ---
    def test_validate_registration_success_valid_data(self):
        result, msg = validate_registration("user_123", "Пароль1!", "Пароль1!")
        self.assertTrue(result)
        self.assertEqual(msg, "")

    def test_validate_registration_fails_empty_login(self):
        result, msg = validate_registration("", "Пароль1!", "Пароль1!")
        self.assertFalse(result)
        self.assertEqual(msg, "Логин не может быть пустым")

    def test_validate_registration_fails_blacklisted_login(self):
        result, msg = validate_registration("admin", "Пароль1!", "Пароль1!")
        self.assertFalse(result)
        self.assertEqual(msg, "Логин находится в черном списке")

    def test_validate_registration_fails_invalid_login_format(self):
        result, msg = validate_registration("bad login!", "Пароль1!", "Пароль1!")
        self.assertFalse(result)
        self.assertIn("Логин не соответствует формату", msg)

    def test_validate_registration_fails_empty_password(self):
        result, msg = validate_registration("user_123", "", "")
        self.assertFalse(result)
        self.assertEqual(msg, "Пароль не может быть пустым")

    def test_validate_registration_fails_short_password(self):
        result, msg = validate_registration("user_123", "П1!", "П1!")
        self.assertFalse(result)
        self.assertEqual(msg, "Пароль должен содержать минимум 7 символов")

    def test_validate_registration_fails_invalid_character_in_password(self):
        result, msg = validate_registration("user_123", "Password1!", "Password1!")
        self.assertFalse(result)
        self.assertIn("недопустимые символы", msg)

    def test_validate_registration_fails_no_uppercase_cyrillic(self):
        result, msg = validate_registration("user_123", "пароль1!", "пароль1!")
        self.assertFalse(result)
        self.assertEqual(msg, "Пароль должен содержать хотя бы одну заглавную кириллическую букву")

    def test_validate_registration_fails_no_lowercase_cyrillic(self):
        result, msg = validate_registration("user_123", "ПАРОЛЬ1!", "ПАРОЛЬ1!")
        self.assertFalse(result)
        self.assertEqual(msg, "Пароль должен содержать хотя бы одну строчную кириллическую букву")

    def test_validate_registration_fails_no_digit(self):
        result, msg = validate_registration("user_123", "Пароль!", "Пароль!")
        self.assertFalse(result)
        self.assertEqual(msg, "Пароль должен содержать хотя бы одну цифру")

    def test_validate_registration_fails_no_special_char(self):
        result, msg = validate_registration("user_123", "Пароль1", "Пароль1")
        self.assertFalse(result)
        self.assertEqual(msg, "Пароль должен содержать хотя бы один спецсимвол")

    def test_validate_registration_fails_password_mismatch(self):
        result, msg = validate_registration("user_123", "Пароль1!", "Пароль2!")
        self.assertFalse(result)
        self.assertEqual(msg, "Пароль и подтверждение пароля не совпадают")

if __name__ == '__main__':
    unittest.main()
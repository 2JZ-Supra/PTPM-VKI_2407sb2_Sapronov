import logging
import sys
import os
import re
import hashlib

BLACKLIST = {
    "admin", "root", "user", "test", "guest",
    "qwerty", "12345", "password", "moderator", "support"
}


def mask_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()[:8]


def is_phone(login: str) -> bool:
    return re.fullmatch(r"\+\d-\d{3}-\d{3}-\d{4}", login) is not None


def is_email(login: str) -> bool:
    return re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", login) is not None


def is_plain_login(login: str) -> bool:
    return re.fullmatch(r"[a-zA-Z0-9_]{5,}", login) is not None


def validate_registration(login: str, password: str, confirm: str):
    if not login:
        return False, "Логин не может быть пустым"

    if login.lower() in BLACKLIST:
        return False, "Логин находится в черном списке"

    if not (is_phone(login) or is_email(login) or is_plain_login(login)):
        return False, (
            "Логин не соответствует формату телефона, email или обычной строки "
            "(мин. 5 символов, латиница, цифры, _)"
        )

    if not password:
        return False, "Пароль не может быть пустым"

    if len(password) < 7:
        return False, "Пароль должен содержать минимум 7 символов"

    allowed_special = set("!@#$%^&*()-_=+[]{};:'\",.<>/?\\|`~")

    for ch in password:
        if not (
            ch.isdigit()
            or ch in allowed_special
            or ('А' <= ch <= 'я')
            or ch in ('Ё', 'ё')
        ):
            return False, "Пароль содержит недопустимые символы (разрешены только кириллица, цифры и спецсимволы)"

    if not any('А' <= ch <= 'Я' or ch == 'Ё' for ch in password):
        return False, "Пароль должен содержать хотя бы одну заглавную кириллическую букву"

    if not any('а' <= ch <= 'я' or ch == 'ё' for ch in password):
        return False, "Пароль должен содержать хотя бы одну строчную кириллическую букву"

    if not any(ch.isdigit() for ch in password):
        return False, "Пароль должен содержать хотя бы одну цифру"

    if not any(ch in allowed_special for ch in password):
        return False, "Пароль должен содержать хотя бы один спецсимвол"

    if password != confirm:
        return False, "Пароль и подтверждение пароля не совпадают"

    return True, ""
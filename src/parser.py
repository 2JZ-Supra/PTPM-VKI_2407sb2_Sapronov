import re
import requests
from bs4 import BeautifulSoup


class ForumParser:
    BASE_URL = "https://www.woman.ru"
    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    }

    def __init__(self, headers: dict | None = None):
        self.headers = headers or self.DEFAULT_HEADERS

    def get_thread_urls(self, listing_url: str) -> list[str]:
        try:
            response = requests.get(listing_url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка запроса страницы листинга: {e}")
            return []

        soup = BeautifulSoup(response.text, "lxml")

        urls = []

        list_container = soup.find("div", class_="list", attrs={"data-page-index": True})

        if not list_container:
            print(f"Блок с темами не найден на странице: {listing_url}")
            return []

        for a in list_container.find_all("a", class_="list-item__link"):
            href = a.get("href")
            if href and "thread-" in href:
                urls.append(self.BASE_URL + href)

        return urls

    def parse_page(self, url: str) -> dict | None:
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка запроса темы {url}: {e}")
            return None

        soup = BeautifulSoup(response.text, "lxml")

        topic_start = soup.find("div", class_="card_topic-start")
        if not topic_start:
            print(f"Не найден блок card_topic-start на странице {url}")
            return None

        # ID сообщения
        comment_id = topic_start.get("data-id")
        if not comment_id:
            match = re.search(r"id(\d+)", url)
            comment_id = match.group(1) if match else None

        if not comment_id:
            return None

        # Логин автора
        user_name_block = topic_start.find("div", class_="user__name")
        username = user_name_block.get_text(strip=True) if user_name_block else "Аноним"

        # Текст сообщения
        message_block = topic_start.find("div", class_="card__comment")
        message = message_block.decode_contents() if message_block else ""

        if not message:
            return None

        return {"id": int(comment_id), "name": username, "message": message}

    def save_to_db(self, parsed_data: dict, repository) -> bool:
        if not parsed_data:
            return False
        return repository.add(
            comment_id=parsed_data["id"],
            username=parsed_data["name"],
            message=parsed_data["message"],
        )
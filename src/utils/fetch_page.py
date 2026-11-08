import requests


def fetch_html():
    url = "https://www.woman.ru/forum/?sort=new"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    }

    try:
        print(f"Загружаем страницу: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        with open("some_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        print("✅ Успех! HTML-код сохранен в файл 'some_page.html'.")

    except requests.RequestException as e:
        print(f"❌ Ошибка при загрузке: {e}")


if __name__ == "__main__":
    fetch_html()
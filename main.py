import random
import time
from src.database import DatabaseRepository
from src.parser import ForumParser


def main():
    db_file = "forum.db"
    repo = DatabaseRepository(db_file)
    print(f"База данных инициализирована: {db_file}")

    parser = ForumParser()

    base_url = "https://www.woman.ru/forum/"
    pages_to_scrape = 1

    all_thread_urls = set()

    for page_num in range(1, pages_to_scrape + 1):
        if page_num == 1:
            url = f"{base_url}?sort=new"
        else:
            url = f"{base_url}{page_num}/?sort=new"

        print(f"\nПолучаем список тем со страницы {page_num}: {url}")
        urls = parser.get_thread_urls(url)

        if not urls:
            print(f"Темы на странице {page_num} не найдены. Возможно, страницы закончились.")
            break

        print(f"✅ Найдено тем на странице {page_num}: {len(urls)}")
        all_thread_urls.update(urls)

        time.sleep(random.uniform(1.5, 4.0))

    print(f"\n🎉 Всего найдено уникальных тем для парсинга: {len(all_thread_urls)}")
    print("Начинаем парсинг каждой темы...\n")

    saved_count = 0
    for i, url in enumerate(all_thread_urls, 1):
        print(f"[{i}/{len(all_thread_urls)}] Парсим: {url}")
        parsed_data = parser.parse_page(url)

        if parsed_data:
            success = parser.save_to_db(parsed_data, repo)
            if success:
                print(f"  ✅ Сохранено сообщение ID: {parsed_data['id']} (Автор: {parsed_data['name']})")
                saved_count += 1
            else:
                print(f"  ⚠️ Не удалось сохранить (возможно, запись с таким ID уже существует).")
        else:
            print(f"  ❌ Не удалось спарсить тему.")

        time.sleep(1)

    print(f"\n🏁 Готово! Сохранено новых записей: {saved_count} из {len(all_thread_urls)}.")


if __name__ == "__main__":
    main()
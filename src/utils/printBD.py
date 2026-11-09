import os
import argparse
import textwrap
from src.database import DatabaseRepository


def print_records(records: list, limit: int):
    if not records:
        print("База данных пуста. Сначала запустите main.py.")
        return

    to_show = records[:limit]

    print(f"Всего записей в БД: {len(records)}")
    print(f"Первые {len(to_show)} записей из {len(records)}")

    for i, rec in enumerate(to_show, 1):
        short_message = textwrap.shorten(rec["message"], width=200, placeholder="...")

        print(f"\n[Запись #{i}]")
        print(f"  🆔 ID:       {rec['id']}")
        print(f"  👤 Автор:    {rec['name']}")
        print(f"  💬 Сообщение: {short_message}")

    if len(records) > limit:
        print()
        print(f"ℹ️ Показано {len(to_show)} из {len(records)} записей.")
        print("   Чтобы увидеть все, запустите: python view_db.py --all")
        print("   Или укажите свой лимит:       python view_db.py --limit 50")
    else:
        print()
        print(f"✅ Показаны все записи из базы. Всего: {len(to_show)}.")

def main():
    parser = argparse.ArgumentParser(description="Вывод содержимого БД в консоль.")
    parser.add_argument("--limit", type=int, default=10, help="Лимит записей.")
    parser.add_argument("--all", action="store_true", help="Вывести все записи.")
    parser.add_argument("--db", type=str, default="forum.db", help="Путь к файлу БД.")
    args = parser.parse_args()

    db_path = os.path.abspath(args.db)

    if not os.path.exists(db_path):
        print(f"❌ Файл БД не найден: {db_path}")
        print("Сначала запустите: python main.py")
        return

    repo = DatabaseRepository(db_path)
    records = repo.get_all()

    limit = len(records) if args.all else args.limit
    print_records(records, limit)


if __name__ == "__main__":
    main()
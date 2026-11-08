import requests
import unittest
from unittest.mock import patch, Mock
from src.parser import ForumParser
from src.database import DatabaseRepository

# Главная страница
MAIN_PAGE_HTML = """
<html>
  <body>
    <div class="list list_role_independant" data-page-index="1">
      <ul class="list__container">
        <li class="list-item">
          <a class="list-item__link" href="/relations/family/thread-test-id123456/">Тестовая тема 1</a>
        </li>
        <li class="list-item">
          <a class="list-item__link" href="/relations/men/thread-another-id999/">Тестовая тема 2</a>
        </li>
      </ul>
    </div>
  </body>
</html>
"""

# Страница темы
THREAD_PAGE_HTML = """
<html>
  <body>
    <div class="card card_topic-start" data-id="123456">
      <div class="card__text">
        <div class="card__comment">
          <p class="quill-paragraph">Это тестовый текст сообщения.</p>
        </div>
      </div>
      <div class="card__user">
        <div class="user__name">Мария</div>
      </div>
    </div>
  </body>
</html>
"""


class TestForumParser(unittest.TestCase):
    def setUp(self):
        self.parser = ForumParser()
        self.repo = DatabaseRepository(":memory:")

    @patch("src.parser.requests.get")
    def test_get_thread_urls(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = MAIN_PAGE_HTML
        mock_get.return_value = mock_response

        urls = self.parser.get_thread_urls("https://www.woman.ru/forum/")

        self.assertEqual(len(urls), 2)
        self.assertIn("https://www.woman.ru/relations/family/thread-test-id123456/", urls)
        self.assertIn("https://www.woman.ru/relations/men/thread-another-id999/", urls)

    @patch("src.parser.requests.get")
    def test_parse_page_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = THREAD_PAGE_HTML
        mock_get.return_value = mock_response

        url = "https://www.woman.ru/relations/family/thread-test-id123456/"
        data = self.parser.parse_page(url)

        self.assertIsNotNone(data)
        self.assertEqual(data["id"], 123456)
        self.assertEqual(data["name"], "Мария")
        self.assertIn("тестовый текст сообщения", data["message"])

    @patch("src.parser.requests.get")
    def test_parse_page_request_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")

        data = self.parser.parse_page("https://example.com")
        self.assertIsNone(data)

    def test_save_to_db(self):
        data = {"id": 123456, "name": "Мария", "message": "Текст"}
        self.assertTrue(self.parser.save_to_db(data, self.repo))

        saved = self.repo.get_by_id(123456)
        self.assertIsNotNone(saved)
        self.assertEqual(saved["name"], "Мария")


if __name__ == "__main__":
    unittest.main()
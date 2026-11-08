import unittest
from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.repo = DatabaseRepository(":memory:")

    # add
    def test_add_success(self):
        self.assertTrue(self.repo.add(1, "user1", "Привет"))
        self.assertIsNotNone(self.repo.get_by_id(1))

    def test_add_duplicate_id(self):
        self.repo.add(1, "user1", "Привет")
        self.assertFalse(self.repo.add(1, "user2", "Другой текст"))

    # get_by_id
    def test_get_by_id_found(self):
        self.repo.add(1, "user1", "Текст")
        row = self.repo.get_by_id(1)
        self.assertEqual(row["name"], "user1")
        self.assertEqual(row["message"], "Текст")

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.repo.get_by_id(999))

    # get_by_name
    def test_get_by_name_returns_list(self):
        self.repo.add(1, "alice", "A")
        self.repo.add(2, "alice", "B")
        self.repo.add(3, "bob", "C")
        result = self.repo.get_by_name("alice")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["message"], "A")

    def test_get_by_name_empty(self):
        self.assertEqual(self.repo.get_by_name("unknown"), [])

    # update
    def test_update_existing(self):
        self.repo.add(1, "user", "Старый")
        self.assertTrue(self.repo.update(1, "Новый"))
        self.assertEqual(self.repo.get_by_id(1)["message"], "Новый")

    def test_update_non_existing(self):
        self.assertFalse(self.repo.update(999, "Новый"))

    # delete
    def test_delete_existing(self):
        self.repo.add(1, "user", "Текст")
        self.assertTrue(self.repo.delete(1))
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_non_existing(self):
        self.assertFalse(self.repo.delete(999))


if __name__ == "__main__":
    unittest.main()
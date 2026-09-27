import unittest
from src.delivery_service import calculate_delivery_cost

class TestDeliveryService(unittest.TestCase):

    def test_valid_standard_delivery_success(self):
        cost, date = calculate_delivery_cost(2.0, 1000, "обычный", False)
        self.assertEqual(cost, 5200) # 200 + 1000*5 = 5200
        self.assertEqual(date, "2026-09-05") # 1000//500 = 2 дня -> 3 сентября + 2 дня

    def test_weight_no_multiplier_for_light_package(self):
        cost, _ = calculate_delivery_cost(5.0, 500, "обычный")
        self.assertEqual(cost, 2700) # 200 + 500*5 = 2700 (нет наценки за вес)

    def test_weight_multiplier_for_medium_package(self):
        cost, _ = calculate_delivery_cost(10.0, 500, "обычный")
        self.assertEqual(cost, 3240) # (200 + 2500) * 1.2 = 3240

    def test_weight_multiplier_for_heavy_package(self):
        cost, _ = calculate_delivery_cost(20.0, 500, "обычный")
        self.assertEqual(cost, 4050) # (200 + 2500) * 1.5 = 4050

    def test_fragile_package_adds_cost(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "хрупкий")
        self.assertEqual(cost, 1000) # 200 + 500 + 300 = 1000

    def test_dangerous_package_adds_cost(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "опасный")
        self.assertEqual(cost, 1700) # 200 + 500 + 1000 = 1700

    def test_express_delivery_increases_cost(self):
        # Проверяем исправленный баг 1
        std_cost, _ = calculate_delivery_cost(2.0, 1000, "обычный", False)
        exp_cost, _ = calculate_delivery_cost(2.0, 1000, "обычный", True)
        self.assertTrue(exp_cost > std_cost, "Экспресс-доставка должна стоить дороже обычной")
        self.assertEqual(exp_cost, 7800) # 5200 * 1.5 = 7800

    def test_express_delivery_takes_at_least_one_day(self):
        # Проверяем исправленный баг 2
        _, date = calculate_delivery_cost(2.0, 400, "обычный", True)
        self.assertNotEqual(date, "2026-09-03", "Экспресс-доставка не может быть в день отправки")
        self.assertEqual(date, "2026-09-04") # 1 день

    def test_invalid_weight_too_low(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_weight_too_high(self):
        cost, date = calculate_delivery_cost(55.0, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_distance_too_low(self):
        cost, date = calculate_delivery_cost(2.0, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_distance_too_high(self):
        cost, date = calculate_delivery_cost(2.0, 6000, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_package_type(self):
        cost, date = calculate_delivery_cost(2.0, 100, "неизвестный")
        self.assertEqual(cost, -1)

if __name__ == '__main__':
    unittest.main()
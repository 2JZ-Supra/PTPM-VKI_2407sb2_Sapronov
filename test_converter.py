import unittest
from converter import Converter

class TestConverter(unittest.TestCase):

    def test_positive_boundary_and_infinity(self):
        self.assertEqual(Converter.do(100.7), 1000)
        self.assertEqual(Converter.do(150.5), 1000)
        self.assertEqual(Converter.do(9999.9), 1000)

    def test_positive_interval(self):
        self.assertEqual(Converter.do(0.1), 0)
        self.assertEqual(Converter.do(100.6), 100)
        self.assertEqual(Converter.do(65.7), 65)
        self.assertEqual(Converter.do(50.0), 50)

    def test_zero_value_exception(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_negative_interval(self):
        self.assertEqual(Converter.do(-30.4), -35)
        self.assertEqual(Converter.do(-30.3), -35)
        self.assertEqual(Converter.do(-0.1), -5)
        self.assertEqual(Converter.do(-15.8), -20)

    def test_negative_boundary_and_infinity(self):
        self.assertEqual(Converter.do(-30.5), -2000)
        self.assertEqual(Converter.do(-30.6), -2000)
        self.assertEqual(Converter.do(-94.5), -2000)
        self.assertEqual(Converter.do(-1000.0), -2000)

if __name__ == '__main__':
    unittest.main()
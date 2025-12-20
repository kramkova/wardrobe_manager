import unittest
from datetime import date
from src.models import Category, Season, Item, Outfit


class TestItemConstructor(unittest.TestCase):
    def setUp(self):
        self.item = Item(name="синяя рубашка", colour="синий", category=Category.TOP)

    def test_item_init(self):
        self.assertEqual(self.item.name, "синяя рубашка")
        self.assertEqual(self.item.category, Category.TOP)
        self.assertEqual(self.item.colour, "синий")
        self.assertEqual(self.item.season, Season.ALLSEASON)
        self.assertEqual(self.item.start, date.today())
        self.assertEqual(self.item.wear_count, 0)
        self.assertEqual(self.item.brand, None)
        self.assertEqual(self.item.price, None)


class TestOutfitConstructor(unittest.TestCase):
    def setUp(self):
        """Подготовка данных для тестов"""
        self.shirt = Item("Рубашка", Category.TOP, "синий")
        self.jeans = Item("Джинсы", Category.BOTTOM, "чёрный")
        self.items = [1, 2]

    def test_outfit_init(self):
        """Тестируем корректную инициализацию атрибутов Outfit"""
        outfit = Outfit(items=self.items, wear_date=date.today())

        self.assertEqual(outfit.items, self.items)
        self.assertEqual(outfit.date, date.today())


if __name__ == "__main__":
    unittest.main()

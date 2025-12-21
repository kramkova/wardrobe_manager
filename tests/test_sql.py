import unittest

# Неправильные импорты. Следовало так: from your_module import Category, Item, Outfit, Season, SQLAssistant
from src.models import Category, Item, Outfit, Season
from src.sql_engine import SQLAssistant


class TestSQLAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = SQLAssistant(user_name='Paul')
        jeans = Item('basic jeans', Category.BOTTOM, 'blue', Season.ALLSEASON)
        polo = Item('striped polo', Category.TOP, 'red', Season.SUMMER)
        shirt = Item('starred shirt', Category.TOP, 'white', Season.ALLSEASON)
        fit1 = Outfit(items=[1, 2], liked=True)
        fit2 = Outfit(items=[1, 3])
        self.assistant.add_item(jeans)
        self.assistant.add_item(shirt)
        self.assistant.add_item(polo)
        self.assistant.record_outfit(fit1)
        self.assistant.record_outfit(fit2)

    def test_getters(self):
        self.assertEqual(
            self.assistant.get_most_worn_items(1),
            [
                1,
            ],
        )
        self.assertEqual(self.assistant.get_recently_worn_items(), [1, 2, 3])
        self.assertIn(
            1,
            self.assistant.get_items_by_category(Category.BOTTOM),
        )

        wanted_wardrobe = {
            Category.TOP: [2, 3],
            Category.BOTTOM: [
                1,
            ],
        }
        self.assertIsInstance(self.assistant.get_wardrobe(), dict)
        self.assertEqual(
            wanted_wardrobe[Category.TOP][:2],
            self.assistant.get_wardrobe()[Category.TOP][:2],
        )

    def test_build_outfit(self):
        self.assertEqual(self.assistant.build_outfit(base_item=2), [2, 1])


if __name__ == '__main__':
    unittest.main()

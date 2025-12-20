import unittest
from src.sql_engine import SQLAssistant
from src.models import Category, Item, Season, Outfit


class TestSQLAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = SQLAssistant(user_name="Paul")
        jeans = Item("basic jeans", Category.BOTTOM, "blue", Season.ALLSEASON)
        polo = Item("striped polo", Category.TOP, "red", Season.SUMMER)
        shirt = Item("starred shirt", Category.TOP, "white", Season.ALLSEASON)
        fit1 = Outfit(items=[1, 2], liked=True)
        fit2 = Outfit(items=[1, 3])
        self.assistant.add_item(jeans)
        self.assistant.add_item(shirt)
        self.assistant.add_item(polo)
        self.assistant.record_outfit(fit1)
        self.assistant.record_outfit(fit2)
        print(self.assistant.outfit_items)

    def test_user_init(self):
        pass


if __name__ == "__main__":
    unittest.main()

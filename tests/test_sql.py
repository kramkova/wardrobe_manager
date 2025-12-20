import unittest
from src.sql_engine import SQLAssistant
from src.models import Category, Item, Season, Outfit


class TestSQLAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = SQLAssistant(user_name="Paul")
        jeans = Item("basic jeans", Category.BOTTOM, "blue", Season.ALLSEASON)
        shirt = Item("striped polo", Category.TOP, "red", Season.SUMMER)
        fit1 = Outfit(items=[1, 2], liked=True)
        self.assistant.add_item(jeans)
        self.assistant.add_item(shirt)
        self.assistant.record_outfit(fit1)

    def test_user_init(self):
        pass


if __name__ == "__main__":
    unittest.main()

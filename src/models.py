from datetime import date
from enum import Enum
from typing import List


class Category(Enum):
    TOP = 'Верх'
    BOTTOM = 'Низ'
    OVERALLS = 'Костюм'
    LAYER = 'Кофта'
    COAT = 'Верхняя одежда'
    ACCESSORY = 'Аксессуар'
    SHOES = 'Обувь'


class Season(Enum):
    WINTER = 'Зима'
    SUMMER = 'Лето'
    MIDSEASON = 'Демисезон'
    ALLSEASON = 'Круглогодично'


class Item:
    def __init__(self, item_id: int, name: str, category: Category, colour: str, season: Season = Season.ALLSEASON,
                 start: date = date.today(), brand: str = None, price: int = None, wear_count: int = 0):
        self.id = item_id
        self.name = name
        self.category = category
        self.colour = colour
        self.season = season
        self.start = start
        self.brand = brand
        self.price = price
        self.wear_count = wear_count


class Outfit:
    def __init__(self, outfit_id: int, items: List[int], wear_date: date = date.today(), liked: bool = False):
        self.id = outfit_id
        self.items = items
        self.date = wear_date
        self.liked = liked

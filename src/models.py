# Нет и докстрингов

from datetime import date
from enum import Enum
from typing import List  # Такой способ аннотации типа устарел. Вместо него используйте `list[...]`


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


class Style(Enum):
    CASUAL = 'Повседневный'
    SPORT = 'Спортивный'
    FANCY = 'Нарядный'
    WORK = 'Деловой'


class Item:
    def __init__(
        self,
        name: str,
        category: Category,
        colour: str,
        season: Season = Season.ALLSEASON,
        start: date = date.today(),
        brand: str | None = None,
        price: int = 0,
        wear_count: int = 0,
    ):
        self.name = name
        self.category = category
        self.colour = colour
        self.season = season
        self.start = start
        self.brand = brand
        self.price = price
        self.wear_count = wear_count


class Outfit:
    def __init__(
        self,
        items: List[int],
        wear_date: date = date.today(),
        style: Style = Style.CASUAL,
        liked: bool = False,
    ):
        self.items = items
        self.date = wear_date
        self.style = style
        self.liked = liked

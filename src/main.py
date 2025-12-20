from datetime import datetime

from models import Category, Item
from sql_engine import SQLAssistant


def main():
    user = input('Добро пожаловать в сервис Wardrobe Manager!\nВведите ваше имя: ')
    assistant = SQLAssistant(user)

    add_items = input('Добавить новую вещь? (да/нет) ').lower() == 'да'
    while add_items:
        name = input('Название вещи: ')
        category = input('Категория: ')
        colour = input('Цвет: ')
        brand = input('Фирма-производитель (опционально): ')
        price = int(input('Цена (опц.): '))
        start = input('Дата приобретения в формате ГГГГ-ММ-ДД (опционально): ')

        start_date = datetime.strptime(start, '%Y-%m-%d').date()

        assistant.add_item(
            Item(
                name=name,
                category=Category(category),
                colour=colour,
                brand=brand,
                price=price,
                start=start_date,
            )
        )
        add_items = input('Добавить ещё? (да/нет) ').lower() == 'да'

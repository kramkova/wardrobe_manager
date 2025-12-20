from datetime import datetime

from models import Category, Item, Outfit, Season, Style
from sql_engine import SQLAssistant


def main():
    user = input('Добро пожаловать в сервис Wardrobe Manager!\nВведите ваше имя: ')
    assistant = SQLAssistant(user.strip())

    add_items = input('Добавить новую вещь? (да/нет) ').lower() == 'да'
    while add_items:
        name = input('Название вещи: ')
        category = input('Категория: ')
        colour = input('Цвет: ')
        season = input('*Сезон: ')
        brand = input('*Фирма-производитель: ')
        price = int(input('*Цена: '))
        start = input('*Дата приобретения (ГГГГ-ММ-ДД): ')

        start_date = datetime.strptime(start, '%Y-%m-%d').date()

        assistant.add_item(
            Item(
                name=name,
                category=Category(category),
                colour=colour,
                brand=brand,
                season=Season(season),
                price=price,
                start=start_date,
            )
        )
        print(f'Добавлена новая вещь: {name}')
        add_items = input('Добавить ещё? (да/нет) ').lower() == 'да'

    wardrobe = assistant.get_wardrobe()
    print('Ваш гардероб: ')
    for shelf in wardrobe.items():
        print(f'{shelf[0].value}: {shelf[1]}')

    add_outfits = input('Записать новый образ? (да/нет) ').lower() == 'да'
    while add_outfits:
        items = input('Список id вещей через запятую: ')
        items = [int(i) for i in items.split(sep=', ')]
        style = input('*Стиль: ')
        wear_date = input('*Дата (ГГГГ-ММ-ДД): ')
        wear_date = datetime.strptime(wear_date, '%Y-%m-%d').date()
        liked = input('Добавить в избранное? (да/нет) ').lower() == 'да'

        assistant.record_outfit(Outfit(items=items, style=Style(style), wear_date=wear_date, liked=liked))
        print(f'Добавлена новая запись: {wear_date} - {items}')
        add_outfits = input('Записать ещё? (да/нет) ').lower() == 'да'

    recommend_outfit = input('Добавить новую вещь? (да/нет) ').lower() == 'да'
    while recommend_outfit:
        base_item = int(input('*Id главной вещи в образе: '))
        explorativity = float(input('*Насколько вы готовы к экспериментам по шкале от 0 до 1? '))

        print('Попробуйте это сочетание: ', assistant.build_outfit(base_item=base_item, explorativity=explorativity))

    stats = assistant.get_statistics()
    print('Отчёт о ваших вещах и привычках:')
    for metric in stats:
        print(f'{metric[0]}: {metric[1]}')

from datetime import datetime

from models import Category, Item, Outfit, Season, Style
from sql_engine import SQLAssistant


def add_item(service: SQLAssistant):
    add_items = input('Добавить новую вещь? (да/нет) ').lower() == 'да'
    while add_items:
        name = input('Название вещи: ')
        category = input('Категория: (Верх/Низ/Костюм/Кофта/Верхняя одежда/Обувь/Аксессуар) ')
        colour = input('Цвет: ')
        season = input('*Сезон: (Лето/Зима/Демисезон/Круглогодично) ')
        if not season:
            season = 'Круглогодично'
        brand = input('*Фирма-производитель: ')
        price = input('*Цена: ')
        if price:
            price = int(price)
        start = input('*Дата приобретения (ГГГГ-ММ-ДД): ')
        start = datetime.strptime(start, '%Y-%m-%d').date() if start else datetime.today()

        service.add_item(
            Item(
                name=name,
                category=Category(category),
                colour=colour,
                brand=brand,
                season=Season(season),
                price=price,
                start=start,
            )
        )
        print(f'Добавлена новая вещь: {name}')
        add_items = input('Добавить ещё? (да/нет) ').lower() == 'да'


def get_wardrobe(service: SQLAssistant):
    wardrobe = service.get_wardrobe()
    print('Ваш гардероб: ')
    for shelf in wardrobe.items():
        print(f'{shelf[0].value}: {shelf[1]}')


def record_outfit(service: SQLAssistant):
    add_outfits = input('Записать новый образ? (да/нет) ').lower() == 'да'
    while add_outfits:
        items = input('Список id вещей через запятую: ')
        items = [int(i) for i in items.split(sep=', ')]
        style = input('*Стиль: (Повседневный/Деловой/Нарядный/Спортивный)')
        if not style:
            style = Style.CASUAL
        wear_date = input('*Дата (ГГГГ-ММ-ДД): ')
        wear_date = datetime.strptime(wear_date, '%Y-%m-%d').date() if wear_date else datetime.today()
        liked = input('Добавить в избранное? (да/нет) ').lower() == 'да'

        service.record_outfit(Outfit(items=items, style=Style(style), wear_date=wear_date, liked=liked))
        print(f'Добавлена новая запись: {wear_date} - {items}')
        add_outfits = input('Записать ещё? (да/нет) ').lower() == 'да'


def recommend(service: SQLAssistant):
    recommend_outfit = input('Получить рекомендацию образа? (да/нет) ').lower() == 'да'
    while recommend_outfit:
        base_item = int(input('*Id главной вещи в образе: '))
        explorativity = float(input('*Насколько вы готовы к экспериментам по шкале от 0 до 1? '))

        print('Попробуйте это сочетание: ', service.build_outfit(base_item=base_item, explorativity=explorativity))
        recommend_outfit = input('Рекомендовать ещё? (да/нет) ').lower() == 'да'


def get_report(service: SQLAssistant):
    stats = service.get_statistics()
    print('Отчёт о ваших вещах и привычках:')
    for metric in stats:
        print(f'{metric[0]}: {metric[1]}')


def main():
    user = input('Добро пожаловать в сервис Wardrobe Manager!\nВведите ваше имя: ')
    assistant = SQLAssistant(user.strip())

    add_item(assistant)
    get_wardrobe(assistant)
    record_outfit(assistant)
    recommend(assistant)
    get_report(assistant)


if __name__ == '__main__':
    main()

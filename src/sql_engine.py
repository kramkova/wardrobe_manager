import os
import random
import sqlite3
from collections import defaultdict
from datetime import date, timedelta
from src.models import Category, Item, Outfit
from typing import List


class SQLAssistant:
    def __init__(self, user_name: str):
        self.name = user_name
        self.database = os.path.join(os.getcwd(), f"databases/{self.name}.db")

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        # Создание системы таблиц при необходимости
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        season TEXT NOT NULL,
        colour TEXT,
        brand TEXT,
        price INTEGER,
        start TEXT,
        wear_count INTEGER
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS outfits (
        id INTEGER PRIMARY KEY,
        wear_date TEXT,
        style TEXT,
        liked BOOLEAN)
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS matching (
        outfit_id INTEGER,
        item_id INTEGER)
        """)

        # Извлечение идентификаторов всех вещей и аутфитов
        cursor.execute("SELECT id FROM items")
        self.items = list(i[0] for i in cursor.fetchall())
        cursor.execute("SELECT id FROM outfits")
        self.outfits = list(i[0] for i in cursor.fetchall())

        # Создание словаря аутфитов
        cursor.execute("SELECT * FROM matching")
        matches = list(cursor.fetchall())
        self.outfit_items = defaultdict(list)
        for match in matches:
            self.outfit_items[match[0]].append(match[1])

        # Извлечение избранных аутфитов
        cursor.execute("SELECT id FROM outfits WHERE liked == True")
        self.liked = list(cursor.fetchall())

        conn.commit()
        conn.close()

    def add_item(self, item: Item):
        with sqlite3.connect(self.database) as conn:
            if not self.items:
                item_id = 0
            else:
                item_id = max(self.items) + 1
            self.items.append(item_id)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (id, name, category, season, colour, brand, price, start, wear_count)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    item_id,
                    item.name,
                    item.category.value,
                    item.season.value,
                    item.colour,
                    item.brand,
                    item.price,
                    item.start.strftime("%Y-%m-%d"),
                    item.wear_count,
                ),
            )

    def record_outfit(self, outfit: Outfit):
        with sqlite3.connect(self.database) as conn:
            if not self.outfits:
                outfit_id = 1
            else:
                outfit_id = max(self.outfits) + 1
            self.outfits.append(outfit_id)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO outfits (id, wear_date, style, liked) VALUES (?, ?, ?, ?)",
                (
                    outfit_id,
                    outfit.date.strftime("%Y-%m-%d"),
                    outfit.style.value,
                    outfit.liked,
                ),
            )
            for item_id in outfit.items:
                cursor.execute(
                    "INSERT INTO matching (outfit_id, item_id) VALUES (?, ?)",
                    (max(self.outfits), item_id),
                )
                cursor.execute(
                    "UPDATE items SET wear_count = wear_count + 1 WHERE id = ?",
                    (item_id,),
                )

    def _create_cooccurrence_matrix(self) -> dict[dict[int]]:
        """Построение матрицы совместной носки вещей"""
        matrix = defaultdict(int)

        for outfit in self.outfit_items.values():
            for i in range(len(outfit)):
                for j in range(i + 1, len(outfit)):
                    item1, item2 = outfit[i], outfit[j]
                    matrix[item1][item2] += 1
                    matrix[item2][item1] += 1

        return matrix

    def _create_weighted_cooccurrence_matrix(self, weight: int = 3) -> dict[dict[int]]:
        """Построение матрицы совместной носки вещей с повышенным коэффициентом для избранных сочетаний"""
        matrix = defaultdict(int)

        for outfit in self.outfit_items.values():
            score = 1
            if outfit in self.liked:
                score = weight
            for i in range(len(outfit)):
                for j in range(i + 1, len(outfit)):
                    item1, item2 = outfit[i], outfit[j]
                    matrix[item1][item2] += score
                    matrix[item2][item1] += score

        return matrix

    def _calculate_compatibility(self, item1: int, item2: int):
        pass

    def get_items_by_category(self, category: Category) -> list[int]:
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM items WHERE category == ?", (category.value,)
            )
            return cursor.fetchall()

    def get_recently_worn_items(self, days: int = 7) -> list[int]:
        interval_start = date(date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM outfits WHERE wear_date > ?", interval_start)
            recent_outfits = cursor.fetchall()

        recent_items = []
        for outfit in recent_outfits:
            recent_items.extend(self.outfit_items[outfit])

        return recent_items

    def get_most_worn_items(self) -> list[int]:
        pass

    def get_underused_worn_items(self) -> list[int]:
        pass

    def build_outfit(self, explorativity: float = 0.0) -> List[int]:
        wardrobe = {}
        for category in Category:
            wardrobe[category] = self.get_items_by_category(category)

        # Выбор случайной вещи в качестве основы аутфита
        base_item = random.choice(wardrobe[Category.TOP] + wardrobe[Category.OVERALLS])
        recommendation = [base_item]

        # Сортировка остальных категорий по коэффициенту совместимости (Category.LAYER, Category.BOTTOM, Category.ACCESSORY, Category.COAT, Category.SHOES)
        for category in Category:
            if category in (Category.TOP, Category.OVERALLS):
                continue
            if base_item in wardrobe[Category.OVERALLS] and category == Category.BOTTOM:
                continue

        # Выбор случайной вещи в каждой категории из указанного перцентиля рейтинга

        return recommendation

    def get_statistics(self):
        pass

import os
import sqlite3
from src.models import Item, Outfit


class SQLAssistant:
    def __init__(self, user_name: str):
        self.name = user_name
        self.database = os.path.join(os.getcwd(), f"databases/{self.name}.db")

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

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

        cursor.execute("SELECT MAX(id) FROM items")
        self.items_num = cursor.fetchone()[0]
        cursor.execute("SELECT MAX(id) FROM outfits")
        self.outfits_num = cursor.fetchone()[0]
        if not self.items_num:
            self.items_num = 0
        if not self.outfits_num:
            self.outfits_num = 0

        conn.commit()
        conn.close()

    def add_item(self, item: Item):
        with sqlite3.connect(self.database) as conn:
            self.items_num += 1
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (id, name, category, season, colour, brand, price, start, wear_count)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.items_num,
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
            self.outfits_num += 1
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO outfits (id, wear_date, style, liked) VALUES (?, ?, ?, ?)",
                (
                    self.outfits_num,
                    outfit.date.strftime("%Y-%m-%d"),
                    outfit.style.value,
                    outfit.liked,
                ),
            )
            for item_id in outfit.items:
                cursor.execute(
                    "INSERT INTO matching (outfit_id, item_id) VALUES (?, ?)",
                    (self.outfits_num, item_id),
                )
                cursor.execute(
                    "UPDATE items SET wear_count = wear_count + 1 WHERE id = ?",
                    (item_id,),
                )

    def _create_cooccurrence_matrix(self):
        pass

    def get_items_by_category(self):
        pass

    def get_recently_worn_items(self):
        pass

    def get_most_worn_items(self):
        pass

    def get_underused_worn_items(self):
        pass

    def find_matching_items(self):
        pass

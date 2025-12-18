import sqlite3


class User:
    def __init__(self, name: str):
        self.name = name
        self.db_name = f'data\\{name}.db'
        self.database = sqlite3.connect(self.db_name)

        cursor = self.database.cursor()

        cursor.execute('''
        CREATE TABLE items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        season TEXT NOT NULL,
        colour TEXT,
        brand TEXT,
        price INTEGER,
        start DATE,
        wearcount INTEGER
        )
        ''')
        cursor.execute('''
        CREATE TABLE outfits (
        id INTEGER PRIMARY KEY,
        wear_date DATE,
        liked BOOLEAN)
        ''')
        cursor.execute('''
        CREATE TABLE matching (
        outfit_id INTEGER,
        item_id INTEGER)
        ''')

        self.database.commit()
        self.database.close()

    def add_item(self):
        pass

    def record_outfit(self):
        pass

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

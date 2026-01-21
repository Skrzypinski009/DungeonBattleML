from db.database_manager import DatabaseManager
from create_database import create_tables, fill_database

from ui.app import MLApp


if __name__ == "__main__":
    if not DatabaseManager.is_exist():
        create_tables()
        fill_database()

    MLApp().run()

import os
import sqlite3


class Database:
    def __init__(self, db_name, db_type, path=None):
        self.db_name = db_name.strip()
        self.db_type = db_type.strip().lower()
        # If a path is not specified, assign default path based on type
        if path:
            self.path = path.strip()
        else:
            if self.db_type == "sqlite":
                self.path = os.path.join("data", "sqlite")
            elif self.db_type == "txt":
                self.path = os.path.join("data", "plain")
            else:
                self.path = ""

    def _append_extension(self, extension):
        if not self.db_name.lower().endswith(extension):
            self.db_name += extension

    def _ensure_directory(self):
        # Create directory if it does not exist
        if self.path and not os.path.isdir(self.path):
            os.makedirs(self.path, exist_ok=True)

    def create(self):
        if self.db_type == "sqlite":
            self.create_sqlite_db()
        elif self.db_type == "txt":
            self.create_txt_db()
        else:
            print("Unsupported database type. Use 'sqlite' or 'txt'.")

    def create_sqlite_db(self):
        self._append_extension(".sqlite")
        self._ensure_directory()
        file_path = os.path.join(self.path, self.db_name)
        # Check if file exists and has content
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            response = input(
                f"The file '{file_path}' already exists and contains data. Do you want to overwrite it? (y/n): "
            ).strip().lower()
            if response != 'y':
                print("Operation cancelled.")
                return
        conn = None
        try:
            conn = sqlite3.connect(file_path)
            print(f"SQLite database '{file_path}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating SQLite database: {e}")
        finally:
            if conn:
                conn.close()

    def create_txt_db(self):
        self._append_extension(".txt")
        self._ensure_directory()
        file_path = os.path.join(self.path, self.db_name)
        # Check if file exists and has content
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            response = input(
                f"The file '{file_path}' already exists and contains data. Do you want to overwrite it? (y/n): "
            ).strip().lower()
            if response != 'y':
                print("Operation cancelled.")
                return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("")
            print(f"Text file '{file_path}' created successfully.")
        except Exception as e:
            print(f"Error creating text file: {e}")


def main():
    db_name = input("Enter the name of the database: ").strip()
    db_type = input("Enter the type of the database (sqlite or txt): ").strip().lower()
    use_default_path = input("Use the default path? (y/n): ").strip().lower() == 'y'

    if use_default_path:
        path = None
    else:
        path = input("Specify the path where you want to create the database: ").strip()

    db = Database(db_name, db_type, path)
    db.create()


if __name__ == "__main__":
    main()

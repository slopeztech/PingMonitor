#!/usr/bin/env python3

import os
import configparser


class SiteConfigCreator:
    def __init__(self):
        self.configs_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "sites"))
        if not os.path.exists(self.configs_dir):
            os.makedirs(self.configs_dir)

    def ask_input(self):
        # Gather user input
        site = input("Enter the website name or IP: ").strip()
        protocol = input("Enter the protocol for the check (ping, icmp, http, ...): ").strip().lower()
        storage = input("Enter the storage method (sqlite, plain, ...): ").strip().lower()
        config = {
            "site": site,
            "protocol": protocol,
            "storage": storage
        }
        return config

    def choose_db_file(self):
        # Directory where sqlite files are located
        sqlite_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "sqlite"))
        if not os.path.exists(sqlite_dir):
            print(f"Database directory does not exist: {sqlite_dir}")
            return None

        files = [f for f in os.listdir(sqlite_dir) if f.endswith(".sqlite")]
        if not files:
            print("No sqlite files were found in the directory.")
            return None

        print("Select a sqlite file:")
        for idx, filename in enumerate(files, start=1):
            print(f"{idx}. {filename}")

        selected = None
        while selected is None:
            try:
                choice = int(input("Enter the number of the desired file: ").strip())
                if 1 <= choice <= len(files):
                    selected = os.path.join(sqlite_dir, files[choice - 1])
                else:
                    print("Number out of range, please try again")
            except ValueError:
                print("Invalid input, please enter a number")
        return selected

    def save_config(self, config):
        # Use the site name for the file, with extension .conf
        safe_site = config["site"].replace(" ", "_").replace("/", "_")
        filename = os.path.join(self.configs_dir, f"{safe_site}.conf")

        # Configure the file in a format compatible with configparser
        parser = configparser.ConfigParser()
        parser["SiteConfig"] = {
            "site": config["site"],
            "protocol": config["protocol"],
            "storage": config["storage"]
        }
        # Add the storage file path if available
        if config.get("storage_file"):
            parser["SiteConfig"]["storage_file"] = config["storage_file"]

        with open(filename, "w", encoding="utf-8") as f:
            parser.write(f)
        print(f"Configuration file created at: {filename}")

    def run(self):
        config = self.ask_input()
        if config["storage"] == "sqlite":
            db_file = self.choose_db_file()
            if db_file:
                config["storage_file"] = db_file
            else:
                print("No sqlite file selected. Continuing without a database file.")
        self.save_config(config)


def main():
    creator = SiteConfigCreator()
    creator.run()


if __name__ == "__main__":
    main()

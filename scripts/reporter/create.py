#!/usr/bin/env python3

import os
import sys
from typing import List, Optional


class ReporterCreator:
    def __init__(self):
        # Get the base directory (project root)
        if getattr(sys, 'frozen', False):
            # If running as compiled executable
            self.base_dir = os.path.dirname(sys.executable)
        else:
            # If running as script
            self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        self.sites_dir = os.path.join(self.base_dir, "sites")
        self.available_reporters = {
            "1": "Telegram"
        }

    def get_site_configs(self) -> List[str]:
        """Get list of site configuration files."""
        if not os.path.exists(self.sites_dir):
            print(f"Error: Sites directory not found at {self.sites_dir}")
            return []
            
        configs = []
        for file in os.listdir(self.sites_dir):
            if file.endswith(".conf"):
                configs.append(file[:-5])  # Remove .conf extension
        return sorted(configs)

    def select_site(self) -> Optional[str]:
        """Show site list and let user select one."""
        configs = self.get_site_configs()
        if not configs:
            print("No site configurations found.")
            return None

        print("\nAvailable sites:")
        for i, site in enumerate(configs, 1):
            print(f"{i}. {site}")

        while True:
            try:
                choice = input("\nSelect a site number (or 'q' to quit): ")
                if choice.lower() == 'q':
                    return None
                
                index = int(choice) - 1
                if 0 <= index < len(configs):
                    return configs[index]
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def select_reporter(self) -> Optional[str]:
        """Show reporter types and let user select one."""
        print("\nAvailable reporters:")
        for key, value in self.available_reporters.items():
            print(f"{key}. {value}")

        while True:
            choice = input("\nSelect reporter type (or 'q' to quit): ")
            if choice.lower() == 'q':
                return None
            
            if choice in self.available_reporters:
                return self.available_reporters[choice]
            print("Invalid selection. Please try again.")

    def get_telegram_config(self) -> dict:
        """Get Telegram configuration from user."""
        print("\nTelegram Configuration")
        print("---------------------")
        bot_token = input("Enter bot token: ").strip()
        chat_id = input("Enter chat ID: ").strip()
        
        return {
            "type": "telegram",
            "bot_token": bot_token,
            "chat_id": chat_id
        }

    def add_reporter_to_config(self, site: str, reporter_config: dict) -> bool:
        """Add reporter configuration to site config file."""
        config_path = os.path.join(self.sites_dir, f"{site}.conf")
        
        try:
            # Read existing config
            with open(config_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Add reporter section
            reporter_lines = [
                "\n[reporter]\n",
                f"type = {reporter_config['type']}\n"
            ]
            
            if reporter_config['type'] == 'telegram':
                reporter_lines.extend([
                    f"bot_token = {reporter_config['bot_token']}\n",
                    f"chat_id = {reporter_config['chat_id']}\n"
                ])

            # Write updated config
            with open(config_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
                f.writelines(reporter_lines)

            print(f"\nReporter configuration added to {site}.conf")
            return True

        except Exception as e:
            print(f"Error updating configuration: {e}")
            return False

    def create_reporter(self) -> bool:
        """Main method to create a reporter configuration."""
        # Select site
        site = self.select_site()
        if not site:
            return False

        # Select reporter type
        reporter_type = self.select_reporter()
        if not reporter_type:
            return False

        # Get reporter specific configuration
        reporter_config = None
        if reporter_type == "Telegram":
            reporter_config = self.get_telegram_config()

        if not reporter_config:
            return False

        # Add configuration to site config file
        return self.add_reporter_to_config(site, reporter_config)


def main():
    creator = ReporterCreator()
    creator.create_reporter()


if __name__ == "__main__":
    main()

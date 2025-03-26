#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import socket
from typing import Optional


class PingMonitor:
    def __init__(self):
        self.hostname = self._get_hostname()

    def _get_hostname(self) -> str:
        """Get hostname from config or system."""
        try:
            # Try to read from config file
            config_path = os.path.join("config", "pingmonitor.conf")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith("hostname="):
                            return line.split("=", 1)[1].strip()
        except Exception:
            pass
        
        # If no config or error, use system hostname
        return socket.gethostname()

    def run_script(self, script_name: str) -> None:
        script_path = os.path.join("scripts", script_name) + ".py"
        try:
            subprocess.run([sys.executable, script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")

    def check_site_config(self, site: str) -> None:
        # Build the configuration file path
        config_filename = f"{site}.conf"
        config_path = os.path.join("sites", config_filename)

        if not os.path.exists(config_path):
            print(f"Configuration file '{config_path}' does not exist.")
            return

        config = {}
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Ignore empty lines and comments
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()
        except Exception as e:
            print(f"Error reading configuration file: {e}")
            return

        # Verify required keys are present
        required_keys = ["site", "protocol", "storage"]
        missing_keys = [key for key in required_keys if key not in config]

        if missing_keys:
            print(f"Missing configuration in '{config_path}': {', '.join(missing_keys)}")
        else:
            print(f"The site '{site}' has a valid configuration.")
            # Optionally: display the configuration
            for key in required_keys:
                print(f"{key}: {config[key]}")

    def ping_site(self, site: str) -> None:
        # Build the configuration file path
        config_filename = f"{site}.conf"
        config_path = os.path.join("sites", config_filename)

        if not os.path.exists(config_path):
            print(f"Configuration file '{config_path}' does not exist.")
            return

        config = {}
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Ignore empty lines and comments
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()
        except Exception as e:
            print(f"Error reading configuration file: {e}")
            return

        if "protocol" not in config:
            print(f"Missing protocol in '{site}' configuration")
            return

        protocol = config["protocol"].lower()

        try:
            # Dynamically import the protocol module
            module_name = f"utils.{protocol}"
            protocol_module = __import__(module_name, fromlist=[''])

            # Get the domain or IP of the site
            domain = config.get("site", site)

            # Execute the ping using the specific protocol class
            if protocol == "icmp":
                # For ICMP, we use the ICMPPing class
                pinger = protocol_module.ICMPPing(domain)
                result = pinger.ping()
            else:
                # For other protocols, we try to use the generic ping function
                result = protocol_module.ping(config)

            # TODO: add verbose mode to show ping results
            # print(f"Ping result for {domain} using {protocol}: {result}")
            if config.get("storage", "").lower() == "sqlite":
                try:
                    from data.models.db import PingMonitorDB
                    # Get the database file path
                    db_file = config.get("storage_file")
                    if not db_file:
                        print("Error: SQLite database file not specified in configuration.")
                        return
                    # Initialize database connection and save the result
                    db = PingMonitorDB(db_file)
                    # Add hostname to result
                    result["hostname"] = self.hostname
                    db.store_ping_result(site=domain, protocol=protocol, result=result)
                    # print(f"Result saved to SQLite database: {db_file}")
                    
                    # Check if ping failed and if reporters are configured
                    if not result["success"]:
                        # Look for reporter section in configuration file
                        reporter_section = False
                        reporter_config = {}
                        
                        # Read configuration file to find reporter section
                        config_path = os.path.join("sites", f"{site}.conf")
                        try:
                            with open(config_path, 'r', encoding='utf-8') as f:
                                current_section = None
                                for line in f:
                                    line = line.strip()
                                    if not line or line.startswith("#"):
                                        continue
                                    if line.startswith("[") and line.endswith("]"):
                                        current_section = line[1:-1].lower()
                                    elif current_section == "reporter" and "=" in line:
                                        key, value = line.split("=", 1)
                                        reporter_config[key.strip()] = value.strip()
                                        reporter_section = True
                            
                            if reporter_section and "type" in reporter_config:
                                reporter_type = reporter_config["type"].lower()
                                
                                # Send notification based on reporter type
                                if reporter_type == "telegram":
                                    try:
                                        from reporters.telegram import TelegramReporter
                                        bot_token = reporter_config["bot_token"]
                                        chat_id = reporter_config["chat_id"]
                                        reporter = TelegramReporter(bot_token, chat_id)
                                        message = (
                                            f"⚠️ Ping Error Detected\n"
                                            f"Host: {self.hostname}\n"
                                            f"Site: {domain}\n"
                                            f"Protocol: {protocol}\n"
                                            f"Error: {result.get('error_message', 'Unknown error')}"
                                        )
                                        reporter._send_message(message)
                                    except Exception as reporter_error:
                                        print(f"Error sending Telegram notification: {reporter_error}")
                        except Exception as config_error:
                            print(f"Error reading reporter configuration: {config_error}")
                except Exception as db_error:
                    print(f"Error saving to database: {db_error}")
        except ImportError:
            print(f"Could not import module for protocol '{protocol}'")
        except Exception as e:
            print(f"Error performing ping: {e}")


def main():
    monitor = PingMonitor()

    parser = argparse.ArgumentParser(description="Ping Monitor Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    parser_run = subparsers.add_parser("runscript", help="Execute a script")
    parser_run.add_argument("script_name", type=str, help='Script name, e.g., "database/create"')

    parser_check = subparsers.add_parser("check", help="Check a site configuration")
    parser_check.add_argument("site", type=str, help="Site name (configuration file at sites/<site>.conf)")

    parser_ping = subparsers.add_parser("ping", help="Ping a site")
    parser_ping.add_argument("site", type=str, help="Site to ping (e.g., domain name or IP)")

    args = parser.parse_args()

    if args.command == "runscript":
        monitor.run_script(args.script_name)
    elif args.command == "check":
        monitor.check_site_config(args.site)
    elif args.command == "ping":
        monitor.ping_site(args.site)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

import requests
from typing import Optional, Dict, Any
from datetime import datetime


class TelegramReporter:
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize the Telegram reporter.

        Args:
            bot_token (str): Telegram bot token
            chat_id (str): Telegram chat ID where messages will be sent
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def _send_message(self, message: str) -> bool:
        """
        Send a message to Telegram.

        Args:
            message (str): Message to send

        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return False

    def format_ping_message(self, site: str, protocol: str, result: Dict[str, Any]) -> str:
        """
        Format the ping result into a readable message.

        Args:
            site (str): The site that was pinged
            protocol (str): The protocol used
            result (dict): The ping result

        Returns:
            str: Formatted message
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "✅ Success" if result.get('success') else "❌ Failed"
        
        message = [
            f"<b>Ping Monitor Alert</b>",
            f"Time: {timestamp}",
            f"Site: {site}",
            f"Protocol: {protocol}",
            f"Status: {status}"
        ]

        if result.get('success'):
            message.append(f"Response Time: {result.get('response_time_ms')}ms")
        else:
            message.append(f"Error: {result.get('error_message', 'Unknown error')}")

        return "\n".join(message)

    def report_ping_result(self, site: str, protocol: str, result: Dict[str, Any]) -> bool:
        """
        Report a ping result to Telegram.

        Args:
            site (str): The site that was pinged
            protocol (str): The protocol used
            result (dict): The ping result

        Returns:
            bool: True if report was sent successfully, False otherwise
        """
        # Only report failed pings
        if result.get('success'):
            return True

        message = self.format_ping_message(site, protocol, result)
        return self._send_message(message)

    def report_ping_history(self, site: str, protocol: str, results: list, limit: int = 5) -> bool:
        """
        Report a summary of recent ping results.

        Args:
            site (str): The site that was pinged
            protocol (str): The protocol used
            results (list): List of ping results
            limit (int): Maximum number of results to include

        Returns:
            bool: True if report was sent successfully, False otherwise
        """
        if not results:
            return True

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = [
            f"<b>Ping Monitor Summary</b>",
            f"Time: {timestamp}",
            f"Site: {site}",
            f"Protocol: {protocol}",
            f"Recent Results:",
            ""
        ]

        # Add recent results
        for result in results[:limit]:
            status = "✅" if result.success else "❌"
            time_str = result.timestamp.strftime("%H:%M:%S")
            message.append(f"{status} {time_str} - {result.response_time_ms}ms")

        return self._send_message("\n".join(message))

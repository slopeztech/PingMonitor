import socket
import time


class PortPing:
    def __init__(self, host, port=80, timeout=3):
        self.host = host
        self.port = port
        self.timeout = timeout

    def ping(self):
        start_time = time.time()
        try:
            with socket.create_connection((self.host, self.port), self.timeout) as conn:
                response_time = time.time() - start_time  # Tiempo en segundos
                ip = conn.getpeername()[0]
                return {
                    "success": True,
                    "ip": ip,
                    "response_time_sec": response_time
                }
        except (socket.timeout, socket.error):
            return {
                "success": False,
                "ip": None,
                "response_time_sec": None
            }

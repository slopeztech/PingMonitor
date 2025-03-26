import socket
import time


class DNSPing:
    def __init__(self, host):
        self.host = host
        self.result = self.ping()

    def ping(self):
        start_time = time.perf_counter()
        try:
            ip = socket.gethostbyname(self.host)
            success = True
        except socket.gaierror:
            ip = None
            success = False
        response_time = (time.perf_counter() - start_time) * 1000
        return {
            "success": success,
            "ip": ip,
            "response_time_ms": response_time
        }

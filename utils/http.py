import requests
import time


class HTTPPing:
    def __init__(self, target):
        if target.startswith("http://") or target.startswith("https://"):
            self.target = target
        else:
            self.target = "http://" + target

    def ping(self):
        success = False
        response_time = None
        http_code = None

        try:
            start = time.time()
            r = requests.get(self.target)
            response_time = time.time() - start
            http_code = r.status_code
            # Se considera exitoso si el código HTTP es 200.
            success = (http_code == 200)
        except requests.RequestException:
            success = False

        return success, response_time, http_code

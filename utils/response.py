import json


class PMResponse:
    def __init__(self, domain, ping_type, status, response_time, **kwargs):
        """
        Initializes a PingManagerResponse.

        Args:
            domain (str): Domain or IP address of the ping.
            ping_type (str): Type of ping (e.g., ICMP, TCP, etc.).
            status (str): Status of the ping (e.g., "success", "failed").
            response_time (float): Measured response time (e.g., in milliseconds).
            kwargs: Optional additional information.
        """
        self.domain = domain
        self.ping_type = ping_type
        self.status = status
        self.response_time = response_time
        self.additional_info = kwargs

    def to_json(self):
        data = {
            "domain": self.domain,
            "ping_type": self.ping_type,
            "status": self.status,
            "response_time": self.response_time
        }
        if self.additional_info:
            data.update(self.additional_info)
        return json.dumps(data, ensure_ascii=False, indent=4)

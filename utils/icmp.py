from pythonping import ping as python_ping
import time


class ICMPPing:
    def __init__(self, host):
        self.host = host

    def ping(self, count=1, timeout=1000):
        """
        Sends an ICMP echo request ping multiple times using pythonping.

        Parameters:
            count (int): Number of pings to send (default 1)
            timeout (int): Timeout in milliseconds (default 1000)

        Returns:
            dict: Contains:
              - 'success': Boolean indicating success if at least one ping replies.
              - 'response_time_ms': Minimum response time among received pings, otherwise None.
              - 'output': Execution details with each ping result.
              - 'error': Error message in case of exception.
        """
        try:
            # Convert timeout from milliseconds to seconds
            timeout_sec = timeout / 1000.0
            
            # Perform the ping
            result = python_ping(
                self.host,
                count=count,
                timeout=timeout_sec,
                verbose=False
            )
            
            responses = []
            min_rtt = None
            
            # Process results
            for response in result:
                if response.success:
                    rtt_ms = response.time_elapsed * 1000  # Convert to milliseconds
                    responses.append(f"Reply from {self.host} in {int(rtt_ms)}ms")
                    if min_rtt is None or rtt_ms < min_rtt:
                        min_rtt = rtt_ms
                else:
                    responses.append(f"Request failed: {response.error_message}")

            if responses and min_rtt is not None:
                return {
                    "success": True,
                    "response_time_ms": int(min_rtt),
                    "output": "\n".join(responses),
                }
            else:
                return {
                    "success": False,
                    "response_time_ms": None,
                    "output": "\n".join(responses) if responses else "No responses received.",
                }
        except Exception as e:
            return {
                "success": False,
                "response_time_ms": None,
                "output": f"Error: {str(e)}",
                "error": str(e)
            }

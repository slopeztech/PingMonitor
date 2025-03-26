import socket
import struct
import time
import select
import os


def checksum(source: bytes) -> int:
    total = 0
    count_to = (len(source) // 2) * 2
    count = 0
    while count < count_to:
        this_val = source[count + 1] * 256 + source[count]
        total = total + this_val
        total = total & 0xFFFFFFFF
        count += 2

    if count_to < len(source):
        total += source[-1]
        total = total & 0xFFFFFFFF

    total = (total >> 16) + (total & 0xFFFF)
    total += total >> 16
    answer = ~total & 0xFFFF
    answer = socket.htons(answer)
    return answer


class ICMPPing:
    ICMP_ECHO_REQUEST = 8
    ICMP_ECHO_REPLY = 0

    def __init__(self, host):
        self.host = host

    def ping(self, count=1, timeout=1000):
        """
        Sends an ICMP echo request ping multiple times.

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
            timeout_sec = timeout / 1000.0
            # Create raw socket for ICMP (requires administrative privileges)
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.settimeout(timeout_sec)

            pid = os.getpid() & 0xFFFF  # identifier
            responses = []
            min_rtt = None

            for sequence in range(1, count + 1):
                # Build ICMP header with checksum=0 initially
                header = struct.pack("bbHHh", self.ICMP_ECHO_REQUEST, 0, 0, pid, sequence)
                # Payload: current timestamp (8 bytes)
                data = struct.pack("d", time.time())
                # Calculate checksum
                calc_checksum = checksum(header + data)
                # Rebuild header with correct checksum
                header = struct.pack("bbHHh", self.ICMP_ECHO_REQUEST, 0, calc_checksum, pid, sequence)
                packet = header + data

                start_time = time.time()
                sock.sendto(packet, (self.host, 1))

                try:
                    ready = select.select([sock], [], [], timeout_sec)
                    if not ready[0]:
                        responses.append(f"Request {sequence}: Timeout")
                        continue
                    recv_packet, addr = sock.recvfrom(1024)
                    recv_time = time.time()
                    # The IP header size is variable; typically 20 bytes.
                    # Extract the ICMP header
                    icmp_header = recv_packet[20:28]
                    type_, _code, _recv_checksum, recv_id, _recv_sequence = struct.unpack(
                        "bbHHh", icmp_header
                    )
                    if recv_id == pid and type_ == self.ICMP_ECHO_REPLY:
                        rtt = (recv_time - start_time) * 1000  # in milliseconds
                        responses.append(f"Request {sequence}: Reply from {addr[0]} in {int(rtt)}ms")
                        if min_rtt is None or rtt < min_rtt:
                            min_rtt = rtt
                    else:
                        responses.append(f"Request {sequence}: Invalid reply")
                except socket.timeout:
                    responses.append(f"Request {sequence}: Timeout")
                time.sleep(1)
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
            return {"success": False, "error": str(e)}

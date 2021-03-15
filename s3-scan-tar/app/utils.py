import socket
import time


def sizeof_fmt(size: int) -> str:
    """Convert bytes to human readable units using binary prefix (KiB, MiB), divisble by 1024

    :param int size: size in bytes
    :returns Human readable size
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(size) < 1024.0:
            return "%3.1f %s%s" % (size, unit, "B")
        size /= 1024.0
    return "%.1f%s%s" % (size, "Yi", "B")


def wait_for_port(port, host="localhost", timeout=30.0):
    """Wait until a port starts accepting TCP connections.
    Args:
        port (int): Port number.
        host (str): Host address on which the port should exist.
        timeout (float): In seconds. How long to wait before raising errors.
    Raises:
        TimeoutError: The port isn't accepting connection after time specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(
                    f"Waited too long for the port {port} on host {host} to start accepting connections."
                ) from ex


def fix_encoding(string: str) -> str:
    string.encode(encoding="UTF-8", errors="backslashreplace").decode("utf-8")

    replace_table = {}
    replace_table["\udce6"] = "æ"
    replace_table["\udcf8"] = "ø"
    replace_table["\udce5"] = "å"
    replace_table["\udcc6"] = "Æ"
    replace_table["\udcd8"] = "Ø"
    replace_table["\udcc5"] = "Å"

    for search, replace in replace_table.items():
        string = string.replace(search, replace)

    return string

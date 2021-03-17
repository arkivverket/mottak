import socket
import time


def sizeof_format(size: int) -> str:
    """Convert bytes to human readable units using binary prefix (KiB, MiB), divisble by 1024

    :param int size: size in bytes
    :returns str: Human readable size
    """
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB"]:
        if abs(size) < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} YiB"


def wait_for_port(port: int, host: str = "localhost", timeout: float = 30.0):
    """Wait until a port starts accepting TCP connections.

    :param int port: port number
    :param str host: host address on which the port should exist
    :param float timeout: in seconds, how long to wait before raising errors

    :raises TimeoutError: when the port ins't accepting connection after time specified in `timeout`
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
    """Fixes æøåÆØÅ erros encountered if the file name is latin1 encoding in UTF-8

    :param str string: the string to fix

    :returns str: fixed UTF-8 string
    """
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

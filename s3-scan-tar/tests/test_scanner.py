"""
 - generate a tar file.
 - add a virus to it (EICAR)
 - see if it is detected
"""

import io
import tarfile
from unittest.mock import MagicMock

from pytest import raises
import scanner

BIN_DATA60 = b'012345678901234567890123456789012345678901234567890123456789'
BIN_DATA10 = b'0123456789'
VIRUS = b'VIRUS'


def _generate_tarfile() -> io.BytesIO:
    fh = io.BytesIO(bytearray(1024 * 128))  # 128k buffer.
    tf = tarfile.open(fileobj=fh, mode='w|')
    for i in range(10):
        artificial_file = io.BytesIO(BIN_DATA60 + BIN_DATA60 * i)
        tar_info = tarfile.TarInfo(name=f'file_{i}')
        tar_info.size = len(artificial_file.getbuffer())
        tf.addfile(
            tar_info,
            fileobj=artificial_file
        )
    # add a "virus" to the archive:
    virus_info = tarfile.TarInfo(name='virus.exe')
    virus_info.size = len(VIRUS)
    tf.addfile(virus_info, fileobj=io.BytesIO(VIRUS))
    # close and seek to 0.
    tf.close()
    fh.seek(0)
    return fh


def test_binary_size_limit0():
    fh_base = io.BytesIO(BIN_DATA60 * 10)  # Create a 600 bytes long file.
    fh_limited = scanner.BinaryFileLimitedOnSize(fh_base, maxsize=300)

    chunk = fh_limited.read(10)
    assert chunk == BIN_DATA10
    assert fh_limited.restricted is False
    assert fh_limited.tell() == 10

    # Do a bigger read to trigger the restriction...
    chunk = fh_limited.read(300)
    assert chunk == b''
    assert fh_limited.restricted is True
    assert fh_limited.tell() == 600

    with raises(io.UnsupportedOperation):
        fh_limited.seek(0)


def test_stream_tar():
    fh = _generate_tarfile()
    tar_iterator, t_f = scanner.stream_tar(fh)
    for position, member in enumerate(tar_iterator):
        if position == 10:
            continue
        if not member.isfile():
            continue
        handle = t_f.extractfile(member)
        assert isinstance(handle, io.BufferedReader) is True
        content = handle.read()
        assert content == BIN_DATA60 + BIN_DATA60 * position


def _scan_stream(handle):
    print(f"Scanning stream: {handle}")
    content = b''

    while buffer := handle.read(100):
        content = content + buffer
    if content == VIRUS:
        return {'stream': 'fakevirus'}
    return None


def test_scan_archive(mocker):
    fh = _generate_tarfile()
    magic_socket = MagicMock()
    magic_socket.scan_stream = _scan_stream
    clean, virus, skipped = scanner.scan_archive(fh, magic_socket, 300)
    assert clean == 10
    assert virus == 1
    assert skipped == 7

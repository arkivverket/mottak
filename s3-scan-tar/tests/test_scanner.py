"""
 - generate a tar file.
 - add a virus to it (EICAR)
 - see if it is detected
"""

import io
import tarfile
import logging
from unittest.mock import MagicMock

from pytest import raises
import scanner

BIN_DATA60 = b'012345678901234567890123456789012345678901234567890123456789'
BIN_DATA10 = b'0123456789'
VIRUS = b'VIRUS'


def _generate_tarfile() -> io.BytesIO:
    """ Helper that generates a tar-file on the fly.
    The file will contain files with increasing sizes.
     file_0 : 60 bytes
     file_1 : 120 bytes
     file_2 : 180 bytes
     file_3 : 240 bytes
     file_4 : 300 bytes
     file_9: 600 bytes
     virus.exe : 5 bytes - contains b'VIRUS'

    Returns a file handle.
    """
    fh = io.BytesIO(bytearray(1024 * 128))  # 128k buffer.
    tf = tarfile.open(fileobj=fh, mode='w|')
    for i in range(10):
        # make this increasingly bigger. Note that if i == 0 it is only 60.
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
    """ The the BinaryFileLimitedOnSize class"""
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

    # Seeks throws UnsupportedOperation
    with raises(io.UnsupportedOperation):
        fh_limited.seek(0)


def test_stream_tar():
    """ Tests if we can stream tar files and unpack them """
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
    """ Helper for the mock that mocks the .scanstream method from pyclamd """
    content = b''

    while buffer := handle.read(60):
        content = content + buffer
    if content == VIRUS:
        return {'stream': 'fakevirus'}
    return None


def test_scan_archive():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    """ Tests the scanning of a archive via a filehandle that contains a tar"""
    fh = _generate_tarfile()
    magic_socket = MagicMock()
    magic_socket.scan_stream = _scan_stream
    # Set the restriction to 300 bytes.
    # This should make the 60,120,180,240 and VIRUS pass
    # 300, 360, 420, 480, 540, 600 should be skipped.
    clean, virus, skipped = scanner.scan_archive(fh, magic_socket, 301)
    assert clean == 10
    assert virus == 1
    assert skipped == 6

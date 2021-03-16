"""
 - generate a tar file.
 - add a virus to it (EICAR)
 - see if it is detected
"""

import io
import tarfile
import logging

import pytest
from unittest.mock import Mock


from app.scanner import scan_archive, stream_tar
from app.utils import fix_encoding, sizeof_format
from app.blob import DEFAULT_BUFFER_SIZE

BIN_DATA60 = b'012345678901234567890123456789012345678901234567890123456789'
VIRUS = b'VIRUS'


@pytest.fixture(scope="session", autouse=True)
def _enable_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')


def _generate_tarfile() -> io.BytesIO:
    """ Helper that generates a tar-file on the fly.
    The file will contain files with increasing sizes.
     file_0 : 60 bytes
     file_1 : 120 bytes
     file_2 : 180 bytes
     file_3 : 240 bytes
     file_4 : 300 bytes
     ..
     file_9: 600 bytes
     virus.exe : 5 bytes - contains b'VIRUS'

    Returns a file handle.
    """
    fh = io.BytesIO(bytearray(128 * 1024))  # 128k buffer.
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


def test_stream_tar():
    """ Tests if we can stream tar files and unpack them """
    fh = _generate_tarfile()
    tar_file = stream_tar(fh)
    for position, member in enumerate(tar_file):
        if position == 10:
            continue
        if not member.isfile():
            continue
        handle = tar_file.extractfile(member)
        logging.info(BIN_DATA60)
        assert isinstance(handle, io.BufferedReader) is True
        content = handle.read()
        assert content == BIN_DATA60 + BIN_DATA60 * position


def test_sizeof_format():
    assert sizeof_format(1000) == '1000.0 B'
    assert sizeof_format(1024) == '1.0 KiB'
    assert sizeof_format(255058498) == '243.2 MiB'
    assert sizeof_format(1.930892582e24) == '1.6 YiB'


def test_fix_encoding():
    broken_string = "produksjoner p\345 video/Kolon 3 - \330de \370y.mov"

    assert "produksjoner på video/Kolon 3 - Øde øy.mov" == fix_encoding(broken_string)

    # Check that it doesn't break working UTF-8 encoding
    assert "æøåÆØÅ|æøåÆØÅ" == fix_encoding("\udce6\udcf8\udce5\udcc6\udcd8\udcc5|æøåÆØÅ")
    assert "Ωµ" == fix_encoding("Ωµ")


def _scan_stream(stream, **kwargs):
    """ Helper for the mock that mocks the .scanstream method from pyclamd """
    content = b''

    while buffer := stream.read(60):
        content = content + buffer
    if content == VIRUS:
        return {'stream': 'fakevirus'}
    return None


def _scan_stream_reset(stream, **kwargs):
    """ Helper for the mock that mocks the .scanstream method from pyclamd.
     This one will raise a ConnectionResetError if we go past out limit. Mimicks a
     misconfigured clamd. """
    content = b''
    while buffer := stream.read(60):
        content = content + buffer
        if len(content) + 60 > 300:
            raise ConnectionResetError("Boom!")
    if content == VIRUS:
        return {'stream': 'fakevirus'}
    return None


def test_scan_archive():
    """ Tests the scanning of a archive via a filehandle that contains a tar"""
    fh = _generate_tarfile()
    magic_socket = Mock()
    magic_socket.scan_stream = _scan_stream
    # Set the restriction to 301 bytes.
    # This should make the 60,120,180,240,300 and VIRUS pass
    # 360, 420, 480, 540, 600 should be skipped.
    ret = scan_archive(fh, magic_socket, DEFAULT_BUFFER_SIZE)
    assert ret.clean == 10
    assert ret.virus == 1
    assert ret.skipped == 0


def test_scan_archive_reset():
    """ Tests the scanning of a archive via a filehandle that contains a tar. Trigges resets from clamd."""
    fh = _generate_tarfile()
    magic_socket = Mock()
    magic_socket.scan_stream = _scan_stream_reset
    # Set the restriction to 300 bytes.
    # This should make the 60,120,180,240 and VIRUS pass
    # 300, 360, 420, 480, 540, 600 should be skipped.
    ret = scan_archive(fh, magic_socket, DEFAULT_BUFFER_SIZE)
    assert ret.clean == 4
    assert ret.virus == 1
    assert ret.skipped == 6

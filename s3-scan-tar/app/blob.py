# -*- coding: utf-8 -*-

import io
import logging

from azure.storage.blob import BlobClient
from azure.core.exceptions import ResourceNotFoundError

DEFAULT_BUFFER_SIZE = 4 * 1024 ** 2
WHENCE_START = 0
WHENCE_CURRENT = 1
WHENCE_END = 2
WHENCE_CHOICES = (WHENCE_START, WHENCE_CURRENT, WHENCE_END)

logger = logging.getLogger(__name__)


class _Reader:
    """Read an Azure Blob Storage file."""

    def __init__(self, client: BlobClient, size: int, concurrency: int) -> None:
        self._client = client
        self._size = size
        self._position = 0
        self._concurrency = concurrency

    def seek(self, position: int) -> int:
        self._position = position
        return self._position

    def read(self, size: int) -> bytes:
        if self._position >= self._size:
            return b""

        # Size (length) is recommended for better performance for downlaoding chunks
        if size <= 0 or size is None:
            raise io.UnsupportedOperation(f"{self.__class__.__name__}.read() needs size greater than 0")

        binary = self._client.download_blob(
            offset=self._position,
            max_concurrency=self._concurrency,
            length=size,
        ).readall()

        self._position += len(binary)
        return binary


class _Buffer:
    def __init__(self, buffer_size: int) -> None:
        """Create a _Buffer instance that reads buffer_size bytes when filled."""

        self._buffer_size = buffer_size
        self.empty()

    def __len__(self) -> int:
        """Return the number of unread bytes in the buffer as an int"""
        return len(self._bytes) - self._pos

    def read(self, size: int = -1) -> bytes:
        """Read bytes from the buffer and advance the read position. Returns
        the bytes in a bytestring.

        :optional int size: maximum number of bytes to read.
            If negative or not supplied, read all unread bytes in the buffer

        :returns bytes
        """
        if size < 0 or size > len(self):
            size = len(self)

        part = self._bytes[self._pos: self._pos + size]
        self._pos += len(part)
        return part

    def empty(self) -> None:
        """Remove all bytes from the buffer"""
        self._bytes = b""
        self._pos = 0

    def fill(self, source: _Reader) -> int:
        """Fill the buffer with bytes from source"""

        if self._pos != 0:
            self._bytes = self._bytes[self._pos:]
            self._pos = 0

        if not hasattr(source, "read"):
            raise io.UnsupportedOperation(f"{self.__class__.__name__}.fill() source needs read attribute")
        else:
            new_bytes = source.read(self._buffer_size)

        self._bytes += new_bytes
        return len(new_bytes)


class Blob(io.BufferedIOBase):
    """Reads bytes from Azure Blob Storage"""

    def __init__(
        self,
        client: BlobClient,
        concurrency: int,
        buffer_size: int = DEFAULT_BUFFER_SIZE,
    ) -> None:
        """Reads bytes from Azure Blob Storage

        :param azure.storage.blob.BlobClient client:
        :param int concurrency

        :optional int buffer_size: how much of the stream to store in memory

        :raises azure.core.exceptions.ResourceNotFoundError: Raised when the blob to read from does not exist.
        """

        self.client = client
        if self.client.exists() is False:
            raise ResourceNotFoundError(f"blob {self.client.blob_name} not found in {self.client.container_name}")

        # Acquire a lease on the blob, so that it can not be modified or deleted while we stream it
        # The duration is set to 15 seconds, so if the process were to halt mid-way, the lease will automatically expire
        self._blob_lease = self.client.acquire_lease(lease_duration=15)

        try:
            self.size = self.client.get_blob_properties()["size"]
        except KeyError:
            self.size = 0

        self._reader = _Reader(self.client, self.size, concurrency)
        self._position = 0
        self._buffer = _Buffer(buffer_size)

    # Override some methods from io.IOBase.
    def close(self) -> None:
        """Release the blob lease, flush and close this stream."""
        self._blob_lease.release()
        self._blob_lease = None
        self.client = None
        self._reader = None

    # io.BufferedIOBase methods.
    def seek(self, offset: int, whence: int = WHENCE_START) -> int:
        """Seek to the specified position.

        :param int offset: The offset in bytes.
        :param int whence: Where the offset is from.

        Returns the position after seeking."""
        logger.debug(f"seeking to offset: {offset} whence: {whence}")
        if whence not in WHENCE_CHOICES:
            raise ValueError(f"invalid whence {whence}, expected one of {WHENCE_CHOICES}")

        if whence == WHENCE_START:
            new_position = offset
        elif whence == WHENCE_CURRENT:
            new_position = self._position + offset
        else:
            new_position = self.size + offset
        self._position = new_position
        self._reader.seek(new_position)
        logger.debug(f"current_pos: {self._position}")

        self._buffer.empty()
        return self._position

    def tell(self) -> int:
        """Return the current position within the file."""
        return self._position

    def read(self, size: int) -> bytes:
        """Read up to size bytes from the object and return them."""
        if size == 0:
            return b""

        # Return unused data first
        if len(self._buffer) >= size:
            return self._read_from_buffer(size)

        if self._position == self.size:
            return self._read_from_buffer()

        self._fill_buffer()
        return self._read_from_buffer(size)

    # Internal methods.
    def _read_from_buffer(self, size: int = -1) -> bytes:
        """Remove at most size bytes from our buffer and return them."""
        logger.debug(f"reading {size} bytes from {len(self._buffer)} byte-long buffer")
        size = size if size >= 0 else len(self._buffer)
        part = self._buffer.read(size)
        self._position += len(part)
        # logger.debug(f'part: {part}')
        return part

    def _fill_buffer(self, size=-1):
        # Renew the lease for another 15 seconds
        self._blob_lease.renew()

        size = max(size, self._buffer._buffer_size)
        while len(self._buffer) < size and not self._position == self.size:
            bytes_read = self._buffer.fill(self._reader)
            if bytes_read == 0:
                logger.debug("reached EOF while filling buffer")
                return True

    def __str__(self) -> str:
        return f"({self.__class__.__name__}, {self.client.container_name}, {self.client.blob_name})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(container={self.client.container_name}, blob={self.client.blob_name})"

    # Allows usage in a `with` statement
    def __enter__(self):
        return self

    def __exit__(self, *args) -> None:
        self.close()

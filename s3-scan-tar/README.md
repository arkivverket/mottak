# scan-tar

This takes a tar file and runs it though clamav. It does this by doing a streaming 
read on the file and picks out each element and feeds this to clamav over a socket.

The signatures are refreshed on startup using freshclam.

Environment:
 * CLAMD_SOCK, point to the clamd socket
 * AVLOG, output (report), default /tmp/avlog
 * OBJECT, what to scan, must be a tar file, uncompressed
  

In addition you'll need the ususal stuff to access the objectstore.

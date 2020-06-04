# unpack


this step takes a tar file in a objectstore, streams it and unpacks it on the fly into another objectstore.

it creates a log of the operation that argo can pick up as an artifact.

Inputs:
 * The usual objectstore stuff
 * BUCKET
 * OBJECT, the file to be unpacked
 * UUID, the UUID of the archive

It will attempt to create a blog container in the same storage account named $UUID-0 (IP0, SIP). 
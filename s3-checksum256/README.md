# checksum

This container verifies the checksum of an arbitrary file in the objectstore.

It leaves it's verdicts in /tmp/verdict which is picked up by Argo and used to control the workflow.

Todo:
 * We should generate a proper log artifact that can be logged to the archive-log-service for posterity.


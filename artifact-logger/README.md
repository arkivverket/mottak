This thing picks up files from the local file systems and injects them into the log service. It is mainly ment for prototype use. 
In production you should rather log directly from the service where the artifacts are created.

Usage:

Set the FILES environement variable to a list of files, separates with semicolons.
FILES="/tmp/attachment1.txt;/tmp/attachment2.txt"

It will also look at the UUID env variable to know what UUID these files are attached to.

If the enviroment variable MESSAGE is set it is used as the message. If not, an empty string is logged.

CONDITION is assumed to be "ok", unless set. It can be 'ok', 'warning' or 'error'.


Note that the logger isn't very efficient wrt memory. The contents of each file is copied several times in memory for readability. If these files are big (100s of megabytes) this should be optimizied and it should be streamed into the requests directly.

Note that the content is base64 encoded on the wire.


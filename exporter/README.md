# Exporter

This container sends an archive to preservation.

It uses Azure specific APIs and cannot be used outside Azure. Because of this we don't use our compatibility APIs but rather Microsofts own libs.


## How to run and debug

You need the following enviroment variables set:
 - BUCKET, the bucket you wanna ship over
 - AZURE_ACCOUNT, the account which currently owns the bucket. 
 - AZURE_KEY, the key (password) granting access to the account 
 - AZ_SB_CON_KICKER, the econnection string for the messaging service
 - AZ_SB_QUEUE, the message queue you want to send the message to.



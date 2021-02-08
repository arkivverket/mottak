## Mailer

This container uses mailgun to send a single email. At the moment it looks at the following enviroment variables:
 - RECIPIENT: `<email of the archive submitter>`
 - SUBJECT: `<subject phrase of the email>`
 - MESSAGE: `<Message in the email>`
 - MAILGUN_API_KEY: `<secret used for auth against mailgun>`
 - MAILGUN_DOMAIN: `<some_id>.mailgun.org`

It logs to STDOUT.

Attached is also a tiny utility to look at the status of the last five messages sent.

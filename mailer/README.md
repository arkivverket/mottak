## Mailer

This container uses mailgun to send a single email. At the moment it looks at the following enviroment variables:
```yaml
 - NAME: <recipient's name>
 - RECIPIENT: <recipient's email>
 - SUBJECT: <subject phrase of the email>
 - MESSAGE: <Message in the email>
 - MAILGUN_DOMAIN: <some_id>.mailgun.org
 - MAILGUN_API_KEY: <secret used for auth against mailgun>
 - ATTACHMENTS: <optional path to a list of attached files>
```

It logs to STDOUT.

### mailgun-status.py
[mailgun-statys.py](mailgun-status.py) is a tiny utility to look at the status of the last five messages sent.

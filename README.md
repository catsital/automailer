# Automailer

### Basic Usage

Sending email from Gmail:

```python
from automailer import Mailer
host = smtp.gmail.com
port = 587
sender = foo@bar
name = foo
password = bar
gmail = Mailer(host, port, sender, name, password)
gmail.send(subject, receivers, cc)
```

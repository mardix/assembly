Mail exposes an interface to send email via SMTP or AWS SES.


#### Import

    from mocha import send_mail

#### Send Mail

Send mail helps you quickly send emails.

    template = ""
    to = "me@email.com"

    send_email(template=template, to=to)

#### Mail signals observer

    from mocha import signals

    @signals.send_email.observe
    def my_email_observer():
        pass


#### Mail interface

    from mocha.ext import mail


#### Config

    # AWS SES
    # To use AWS SES to send email
    #:
    #: - To use the default AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    #: set MAIL_URI = "ses://"
    #: * To use a different credential:
    #: set MAIL_URI = "ses://{access_key}:{secret_key}@{region}"
    #:
    #: *** uncomment if you are using SMTP instead
    MAIL_URI = "ses://"

    # SMTP
    #: If you are using SMTP, it will use Flask-Mail
    #: The uri for the smtp connection. It will use Flask-Mail
    #: format: smtp://USERNAME:PASSWORD@HOST:PORT
    #: with sll -> smtp+ssl://USERNAME:PASSWORD@HOST:PORT
    #: with ssl and tls -> smtp+ssl+tls://USERNAME:PASSWORD@HOST:PORT
    #:
    #: *** comment out if you are using SES instead
    # MAIL_URI = "smtp+ssl://{username}:{password}@{host}:{port}"\
    #    .format(username="", password="", host="smtp.gmail.com", port=465)

    #: MAIL_SENDER - The sender of the email by default
    #: For SES, this email must be authorized
    MAIL_SENDER = APPLICATION_ADMIN_EMAIL

    #: MAIL_REPLY_TO
    #: The email to reply to by default
    MAIL_REPLY_TO = APPLICATION_ADMIN_EMAIL

    #: MAIL_TEMPLATE
    #: a directory that contains the email template or a dict
    MAIL_TEMPLATE = os.path.join(APPLICATION_DATA_DIR, "mail-templates")

    #: MAIL_TEMPLATE_CONTEXT
    #: a dict of all context to pass to the email by default
    MAIL_TEMPLATE_CONTEXT = {
        "site_name": APPLICATION_NAME,
        "site_url": APPLICATION_URL
    }


As a convenience, you can use `send_email()` to send email.

    from mocha import Mocha, send_email

    class Index(Mocha):

        @post()
        def send():
            recipient = "email@email.com"
            sender = request.form.get("sender")
            subject = "Welcome"

            mail.send(to=recipient, sender=sender, subject=subet)


Extension: [ses-mailer](https://github.com/mardix/ses-mailer)

Extension: [flask-mail](https://github.com/mattupstate/flask-mail)



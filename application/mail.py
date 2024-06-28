from flask_mail import Mail, Message
from flask import current_app as app
import os
from weasyprint import HTML

mail = Mail(app)

basedir = os.path.abspath(os.path.dirname(__file__))

media_dir = os.path.join(basedir, '../media')


def send_email():

    msg = Message(
        'Hello',
        sender="admin@quentifiedself.com",
        recipients=['email1@example.com','email2@example.com']
    )

    msg.body = "Test Message from <h4> Flask-Mail </h4>"

    msg.html = "<h4> Hello World </h4>"

   

    with app.open_resource(os.path.join(media_dir, 'report.pdf')) as fp:
        msg.attach("report.pdf", "application/pdf", fp.read())

    mail.send(msg)

    return 'Sent'



def send_alert_mail(email):

    msg = Message(
        'Quantified Self daily log alert',
        sender="admin@quentifiedself.com",
        recipients=[email]
    )

    msg.body = "You have no logs today, kindly complete your logging task for today."

    mail.send(msg)

    return 'Sent'


def send_html_report_mail(email, html):

    msg = Message(
        'Quantified Self reports',
        sender="admin@quentifiedself.com",
        recipients=[email]
    )

    msg.html = html

    a = HTML(string=html)

    filename = email.split('@')[0] + '.pdf'

    a.write_pdf(target=os.path.join(media_dir, filename))

    with app.open_resource(os.path.join(media_dir, filename)) as fp:
        msg.attach(filename, "application/pdf", fp.read())

    mail.send(msg)

    return 'Sent'
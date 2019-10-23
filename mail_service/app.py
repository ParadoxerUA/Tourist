from flask import Flask
from flask_mail import Mail, Message
from celery import Celery
from config import MailServiceConfig


app = Flask(__name__)
celery = Celery(app.name, broker='redis://localhost:6379/0')
app.config.from_object(MailServiceConfig)
mail = Mail(app)


@celery.task
def async_email(data):
    with app.app_context():
        msg = Message(subject=data.get('subject'),
            sender=app.config['MAIL_USERNAME'],
            recipients=[data.get('recipient')],
            html=data.get('body'))
        mail.send(msg)


if __name__ == '__main__':
    from urls import *
    app.run(debug=True, port='5001')

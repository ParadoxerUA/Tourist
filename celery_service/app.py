from celery import Celery
from config import MailServiceConfig, CeleryConfig
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import json


mail = smtplib.SMTP(
        host=MailServiceConfig.MAIL_SERVER,
        port=MailServiceConfig.MAIL_PORT
)

app = Celery(
    CeleryConfig.CELERY_APP_NAME,
    broker=CeleryConfig.CELERY_BROKER_URL
)


@app.task
def async_email(data):
    msg = MIMEMultipart()

    msg['From'] = MailServiceConfig.MAIL_USERNAME
    data = json.loads(data)
    msg['To'] = data['recipient']
    msg['Subject'] = data['subject']
    msg.attach(MIMEText(data['body'], 'html'))
    mail.starttls()
    mail.login(msg['From'], MailServiceConfig.MAIL_PASSWORD)
    mail.sendmail(msg['From'], msg['To'], msg.as_string())
    mail.quit()

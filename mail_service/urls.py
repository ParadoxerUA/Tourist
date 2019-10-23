from flask import request
from app import async_email, app
import json


@app.route('/send_email', methods=['POST'])
def send_email():
    request_data = json.loads(request.json)
    recipient = request_data['recipient']
    body = request_data['body']
    subject = request_data['subject']
    data = {
        'body': body,
        'subject': subject,
        'recipient': recipient,
    }
    async_email.delay(data)
    return "OK"

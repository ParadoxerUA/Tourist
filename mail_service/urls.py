from flask import request
from app import async_email, app


@app.route('/send_email', methods=['POST'])
def send_email():
    request_data = request.json
    email = request_data['email']
    body = request_data['body']
    data = {
        'email': email,
        'body': body,
    }
    async_email.delay(data)
    return "OK"

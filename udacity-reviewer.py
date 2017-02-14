from flask import render_template

from app import app, headers
from flask import request
import requests, os


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/notify', methods=['POST'])
def notify():
    fcm_token = request.form['fcm_token']
    data = {}
    if 'url' in request.form:
        data['url'] = request.form['url']
        data['message'] = 'You have been assigned to grade a new submission!'
        data['type'] = 'assignment'
    elif 'created' in request.form:
        data['message'] = 'Request created. Push notification, queue enquiry activated'
        data['type'] = 'activation'
    elif 'closed' in request.form:
        data['message'] = 'Request closed. Push notification, queue enquiry deactivated'
        data['type'] = 'deactivation'
    payload = {
        'to': fcm_token,
        'data': data
    }
    response = requests.post('https://fcm.googleapis.com/fcm/send', json=payload, headers=headers)
    return response.text


@app.route('/register', methods=['POST'])
def register():
    fcm_token = request.form['fcm_token']
    udacity_token = request.form['udacity_token']
    payload = {
        'to': fcm_token,
        'data': {
            'type': 'registration',
            'token': udacity_token
        }
    }
    response = requests.post('https://fcm.googleapis.com/fcm/send', json=payload, headers=headers)
    return response.text


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(port), threaded=True)

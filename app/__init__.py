import os

from flask import Flask

app = Flask(__name__)

headers = {
    'Authorization': 'key=' + os.environ['FCM_SERVER_KEY'],
    'Content-type': 'application/json'
}

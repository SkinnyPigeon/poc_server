from flask import Flask, request, jsonify
from flask_cors import CORS
from mailjet_rest import Client
from dotenv import load_dotenv
import os
import json

project_folder = os.path.expanduser('~/code/pymail/')
load_dotenv(os.path.join(project_folder, '.env'))
api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
CORS(app)

@app.route('/')
def hello():
    return "Hello"

@app.route('/send_results', methods=['post'])
def send():
    req_data = request.get_json()
    print(req_data)

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "euan.blackledge@soprasteria.com",
            "Name": "Euan"
        },
        "To": [
            {
            "Email": "philtheskinnypigeon@yahoo.co.uk",
            "Name": "You"
            }
        ],
        "Subject": "POC Test Dev Results",
        "TextPart": "Here are a set of results from the current POC",
        "HTMLPart": json.dumps(req_data)
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())

    return result.json()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
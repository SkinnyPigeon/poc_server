from flask import Flask, request, jsonify
from flask_cors import CORS
from mailjet_rest import Client
from flask_restplus import Api, Resource, fields
from dotenv import load_dotenv
import os
import json

# project_folder = os.path.expanduser('~/code/api/pymail/')
# load_dotenv(os.path.join(project_folder, '.env'))
api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
CORS(app)
api = Api(
    app, 
    version='1.0', 
    title='Serums POC Server',
    description='Sends the results of the POC to the corresponding use case partner',
)

# Models

hello = api.model('Server Check', {
    'hello': fields.String(required=True, description='Quick check that the server is on', example='Welcome to the POC server. The server is on')
})

question_fields = api.model('Survey Submit', {
    'case_study': fields.String(required=True, description="The name of the use case partner. This is used to pick the email address that will receive the results. The example here selects my one which I am using for testing so as to not clog up everyone else's inboxes", example='TEST'),
    'question': fields.String(required=True, description='The individual questions alongside the submitted answers', example={'q1': {'question': 'Voer uw gebruikers-ID in die door de onderzoeker is verstrekt', 'rating': 123}})
})

response = api.model('Success', {
    'message': fields.String(required=True, description="The automatically generated message by the MailJet API. It contains various elements related to the message including its unique ID", example=[{"Bcc": [], "Cc": [], "CustomID": "", "Status": "success", "To": [{"Email": "123@email.net", "MessageHref": "https://api.mailjet.com/v3/REST/message/288230381147211976", "MessageID": 288230381147211970, "MessageUUID": "b5fb4b4e-b0bd-4cfa-a4c0-687d834cb9c1"}]}])
})

parser = api.parser()
parser.add_argument('Case Study', type=list, required=True, help="The name of the use case partner in upper case", location="json")
parser.add_argument('Question', type=list, required=True, help="The questions that have been answered by the user", location="json")


# Functions

def pick_email(case_study):
    if case_study == 'FCRB':
        email = "jpujoll@clinic.cat"
        name = "Josep"
    elif case_study == 'USTAN':
        email = "tcwds@st-andrews.ac.uk"
        name = "Thais"
    elif case_study == 'ZMC':
        email = "m.mestrum@zuyderland.nl"
        name = "Mark"
    elif case_study == 'TEST':
        email = "2434924@dundee.ac.uk"
        name = "Euan"
    return [email, name]


# Routes
ns = api.namespace('api', description='The Serums POC Server')

@ns.route('/hello')
class ServerCheck(Resource):
    @api.marshal_with(hello)
    def get(self):
        return {"hello": "Welcome to the POC server. The server is on"}


@ns.route('/send_results', methods=['post'])
class SendResults(Resource):
    @api.doc(body=question_fields)
    @api.marshal_with(response, code=200)
    def post(self):
        req_data = request.get_json()
        print(req_data)
        email, name = pick_email(req_data['case_study'])
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
        'Messages': [
            {
            "From": {
                "Email": "2434924@dundee.ac.uk",
                "Name": "Euan"
            },
            "To": [
                {
                "Email": email,
                "Name": name
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
    app.run(debug=True, host='0.0.0.0', port='2021')
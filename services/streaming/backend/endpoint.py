# System
import json

# Third Party
from flask import Blueprint, request, Response, jsonify
from injector import inject
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Local

from services.streaming.lib import StreamingAnalytics
from services.streaming.lib import send_code, authenticate_session
from services.streaming.config import config

blueprint = Blueprint('fnwclient', __name__)

@blueprint.route('/healthz', methods=['GET'])
@inject
def health_check( event=None, context=None ):
    """
    Healthcheck for the service

    An example request might look like:
    .. sourcecode:: http
       GET www.x.com/healthz HTTP/1.1
       Host: example.com
       Accept: application/json, text/javascript

    Results will be returned as JSON object with the following format:

    .. code-block:: json
        {
          "healthy": true
        }
    """

    return Response( json.dumps({'healthy':True}), 200, mimetype='application/json' )

@blueprint.route('/send-code', methods=['POST'])
@inject
def send_code():

    phone_number = config("phone")

    raw_data = request.json()

    if 'phone' not in data:
        return Response( json.dumps({'code-delivered':False}), mimetype='application/json' )

    phone_number = raw_data['phone']
    sent = send_code(**api_creds, phone_number).phone_registered

    return Response( json.dumps({'code-delivered':sent}), mimetype='application/json' )

analytics_module = None

@blueprint.route('/login', methods=['POST'])
@inject
def login():

    api_creds = config("api")
    phone_number = config("phone")

    raw_data = request.json()

    if 'code' not in data:
        return Response( json.dumps({'client-authenticated':False}), mimetype='application/json' )

    code = raw_data['code']
    authenticate_session(**api_creds, **phone_number, code)

    analytics_module = StreamingAnalytics(**api_creds)

    # TODO: check if authenticate_session returns successfully
    return Response( json.dumps({'client-authenticated':True}), mimetype='application/json' )

@blueprint.route('/metrics', methods=['GET'])
@inject
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

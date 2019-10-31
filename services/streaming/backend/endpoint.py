# System
import json

# Third Party
from flask import Blueprint, request, Response, jsonify
from injector import inject
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Local

from services.streaming.lib import StreamingAnalytics
from services.streaming.config import collect_env_vars, config

blueprint = Blueprint('fnwclient', __name__)

creds = config()
analytics_module = StreamingAnalytics(**creds)


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

    return Response( json.dumps({'healthy': True}), 200, mimetype='application/json' )

@blueprint.route('/send-code', methods=['POST'])
@inject
def send_code():

    raw_data = request.json

    if 'phone' not in raw_data:
        return Response(json.dumps({'code-delivered': False}), mimetype='application/json')

    phone_number = raw_data['phone']
    analytics_module.send_code_to_number(phone_number)

    return Response(json.dumps({'code-delivered': True}), mimetype='application/json')

@blueprint.route('/login', methods=['POST'])
@inject
def login():

    # creds = collect_env_vars("API_ID", "API_HASH")
    raw_data = request.json

    if not all (k in raw_data for k in ('code','phone')):
        return Response( json.dumps({'client-authenticated':False}), mimetype='application/json' )

    # code = raw_data['code']
    # phone_number = raw_data['phone']

    code = raw_data['code']
    phone = raw_data['phone']

    analytics_module.authenticate_session(phone, code)
    analytics_module.run()

    # TODO: check if authenticate_session returns successfully
    return Response( json.dumps({'client-authenticated':True}), mimetype='application/json' )

@blueprint.route('/metrics', methods=['GET'])
@inject
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

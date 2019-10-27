# System
import json

# Third Party
from flask import Blueprint, request, Response, jsonify
from injector import inject
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Local

from services.fnwclient.lib import StreamingAnalytics

sa = StreamingAnalytics()

blueprint = Blueprint('fnwclient', __name__)

@blueprint.route('/healthz', methods=['GET'])
@inject
def health_check( event=None, context=None ):
    """
    Healthcheck for the service

    An example request might look like:
    .. sourcecode:: http
       GET www.x.com/example HTTP/1.1
       Host: example.com
       Accept: application/json, text/javascript

    Results will be returned as JSON object with the following format:

    .. code-block:: json
        {
          "healthy": true
        }
    """

    return Response( json.dumps({'healthy':True}), 200, mimetype='application/json' )

@blueprint.route('/metrics', methods=['GET'])
@inject
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

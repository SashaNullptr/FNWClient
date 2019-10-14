# System
import json

# Third Party
from flask import Blueprint, request, Response, jsonify
from injector import inject

# Local
from fnwclient.lib import TelegramAnalytics


blueprint = Blueprint('fnwclient', __name__)

@blueprint.route('/health', methods=['GET'])
@inject
def example_endpoint( event=None, context=None ):
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

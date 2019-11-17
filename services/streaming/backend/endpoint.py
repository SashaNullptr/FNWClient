# System
import json

# Third Party
from flask import Blueprint, request, Response, jsonify
from injector import inject
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

blueprint = Blueprint('fnwclient', __name__)

@blueprint.route('/healthz', methods=['GET'])
@inject
def health_check( event=None, context=None ):


    """

      Check if the service is healthy

    *  **URL Params**

       None

    * **Data Params**

      None

    * **Success Response:**

      **Code:** 200
      **Content:** `{ healthy : true }`

    * **Error Response:**

      **Code:** 404 NOT FOUND
      **Content:** `{ healthy : false }`

    * **Sample Call:**

      .. code-block:: console

        curl -X GET http://0.0.0.0:8080/healthz

    """

    return Response( json.dumps({'healthy': True}), 200, mimetype='application/json' )

@blueprint.route('/metrics', methods=['GET'])
@inject
def metrics():
    """

      Collect latest Prometheus client metrics.

    *  **URL Params**

       None

    * **Data Params**

      None

    * **Sample Call:**

      .. code-block:: console
      
        curl -X GET http://0.0.0.0:8080/metrics

    """
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

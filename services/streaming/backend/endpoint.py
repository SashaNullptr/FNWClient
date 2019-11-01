# System
import json

# Third Party
from flask import Blueprint, request, Response, jsonify
from injector import inject
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Local
from services.streaming.lib import StreamingAnalytics
from services.streaming.config import collect_env_vars

blueprint = Blueprint('fnwclient', __name__)

creds = collect_env_vars("API_ID", "API_HASH")
analytics_module = StreamingAnalytics(**creds)


@blueprint.route('/healthz', methods=['GET'])
@inject
def health_check( event=None, context=None ):


    """

    **Health Check**
    ----
      Check if the service is healthy

    * **URL**

      /healthz/

    * **Method:**

      `GET`

    *  **URL Params**

       None

    * **Data Params**

      None

    * **Success Response:**

      **Code:** 200 <br />
      **Content:** `{ healthy : true }`

    * **Error Response:**

      **Code:** 404 NOT FOUND <br />
      **Content:** `{ healthy : false }`

    * **Sample Call:**

      ```shell
        curl -X GET http://0.0.0.0:8080/healthz
      ```

    """

    return Response( json.dumps({'healthy': True}), 200, mimetype='application/json' )

@blueprint.route('/send-code', methods=['POST'])
@inject
def send_code():
    """

    **Send Code**
    ----
      Send a Telegram client login code to a phone number.

    * **URL**

      /send-code/

    * **Method:**

      `POST`

    *  **URL Params**

       None

    * **Data Params**


       **Required:**

       `phone=[str]`


    * **Success Response:**

      **Code:** 200 <br />
        **Content:** `{ code-sent : true }`

    * **Error Response:**

      **Code:** 404 NOT FOUND <br />
      **Content:** `{ code-sent : false }`

    * **Sample Call:**

      ```shell
        curl -X POST -H "Content-Type: application/json" http://0.0.0.0:8080/send-code -d '{"phone":"+12345678910"}'
      ```

    """

    raw_data = request.json

    if 'phone' not in raw_data:
        return Response(json.dumps({'code-delivered': False}), mimetype='application/json')

    phone_number = raw_data['phone']
    analytics_module.send_code_to_number(phone_number)

    return Response(json.dumps({'code-delivered': True}), mimetype='application/json')

@blueprint.route('/login', methods=['POST'])
@inject
def login():
    """

    **Login**
    ----
      Login to a Telegram client session

    * **URL**

      /login/

    * **Method:**

      `POST`

    *  **URL Params**

       None

    * **Data Params**


       **Required:**

       * `phone=str`
       * `code=str`


    * **Success Response:**

      **Code:** 200 <br />
        **Content:** `{ client-authenticated : true }`

    * **Error Response:**

      **Code:** 404 NOT FOUND <br />
      **Content:** `{ client-authenticated : false }`

    * **Sample Call:**

      ```shell
        curl -X POST -H "Content-Type: application/json" http://0.0.0.0:8080/send-code -d '{"phone":"+12345678910", "code":"123456"}'
      ```

    """

    raw_data = request.json

    if not all (k in raw_data for k in ('code','phone')):
        return Response( json.dumps({'client-authenticated':False}), mimetype='application/json' )

    code = raw_data['code']
    phone = raw_data['phone']

    analytics_module.authenticate_session(phone, code)
    analytics_module.run()

    # TODO: check if authenticate_session returns successfully
    return Response( json.dumps({'client-authenticated':True}), mimetype='application/json' )


@blueprint.route('/metrics', methods=['GET'])
@inject
def metrics():
    """

    **Metrics**
    ----
      Collect latest Prometheus client metrics.

    * **URL**

      /metrics/

    * **Method:**

      `GET`

    *  **URL Params**

       None

    * **Data Params**

      None

    * **Sample Call:**

      ```shell
        curl -X GET http://0.0.0.0:8080/metrics
      ```

    """
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

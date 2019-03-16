# System
import os
import json
import logging
from urllib import parse

# Third Party
from flask import Flask, request, json, redirect, url_for, send_from_directory
from flask_cors import CORS, cross_origin

# Local
from fnwclient.telegram_analytics import TelegramAnalytics

app = Flask(__name__)
CORS(app)

# logging.basicConfig()
# logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def get_answer( event=None, context=None ):

    # Get query string and convert from bytes
    if( request.query_string != None ):

        return app.response_class( json.dumps( {"retval":"merp"} ), mimetype='application/json' )
    else:
        return

if __name__ == '__main__':
    app.run( debug = True )

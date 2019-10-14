from flask import Flask, json
from fnw_client.endpoint import blueprint

app = Flask(__name__)

app.register_blueprint(blueprint)

from flask import Flask

from FNWClient.fnwclient.endpoint.endpoint import blueprint

app = Flask(__name__)

app.register_blueprint(blueprint)

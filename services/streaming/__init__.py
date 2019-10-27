from flask import Flask

from services.fnwclient.backend import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)

from flask import Flask

from services.streaming.backend import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)

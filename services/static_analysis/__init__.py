from flask import Flask

from services.static_analysis.backend import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)

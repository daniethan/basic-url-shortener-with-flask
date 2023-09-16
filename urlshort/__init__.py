from flask import Flask
from decouple import config
from . import urlshort_app


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = config("SECRET_KEY")

    app.register_blueprint(urlshort_app.bp)

    return app

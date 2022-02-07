from ariadne.constants import PLAYGROUND_HTML
from ariadne import graphql_sync
import sensors
from predictor import Predictor
from flask import request, jsonify
import pandas as pd


def register(app, schema):
    @app.route("/")
    def index():
        return "B4BUX Satisfaction Predictor V1.0"

    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        if app.debug:
            return PLAYGROUND_HTML, 200
        return index()

    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(
            schema, data, context_value=request, debug=app.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code

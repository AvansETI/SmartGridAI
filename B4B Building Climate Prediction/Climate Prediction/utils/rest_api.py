from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from utils import Command


class RestApi:
    def __init__(self, host: str = '0.0.0.0', port: int = 8080):
        self._host: str = host
        self._port: int = port

    def run(self, callback_func):
        app = Flask(__name__)
        cors = CORS(app)
        app.config['CORS_HEADERS'] = 'Content-Type'

        @cross_origin()
        @app.route('/convert', methods=['POST'])
        def on_convert():
            print(f'Received new convert call')
            callback_func(Command.CONVERT, dict(request.json))

            return jsonify({}), 200

        @cross_origin()
        @app.route('/generate', methods=['POST'])
        def on_generate():
            print(f'Received new generate call')
            callback_func(Command.GENERATE, dict(request.json))

            return jsonify({}), 200

        @cross_origin()
        @app.route('/train', methods=['POST'])
        def on_train():
            print(f'Received new train call')
            callback_func(Command.TRAIN, dict(request.json))

            return jsonify({}), 200

        @cross_origin()
        @app.route('/predict', methods=['POST'])
        def on_predict():
            print(f'Received new predict call')
            callback_func(Command.PREDICT, dict(request.json))

            return jsonify({}), 200

        app.run(host=self._host, port=self._port, debug=False)

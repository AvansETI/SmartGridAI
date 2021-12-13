import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

from ariadne.constants import PLAYGROUND_HTML
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType

from predict_query import predict_resolver

import sensors
from predictor import Predictor

app = Flask(__name__)
CORS(app)

query = ObjectType("Query")
query.set_field("predict", predict_resolver)

type_defs = load_schema_from_path(f"{ os.path.dirname(os.path.abspath(__file__)) }/schema.graphql")
schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers
)


@app.route("/")
def index():
    return "B4BUX Satisfaction Predictor V1.0"


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


@app.route('/predict', methods=['POST'])
def predict():
    json = request.get_json()

    params = {
        'temperature': sensors.get_temperature(),
        'mean_temp_day': sensors.get_mean_temp_day(),
        'heat_index': sensors.get_heat_index(),
        'relative_humidity': sensors.get_relative_humidity(),
        'light_sensor_one_wave_length': sensors.get_light_sensor_one_wave_length(),
        'light_sensor_two_wave_length': sensors.get_light_sensor_two_wave_length(),
        'number_of_occupants': sensors.get_number_of_occupants(),
        'activity_of_occupants': sensors.get_activity_of_occupants(),
        'state_of_door': sensors.get_state_of_door(),
        'hour': sensors.get_hour(),
        'minute': sensors.get_minute(),
        'second': sensors.get_second(),
    }

    prediction_data = []

    for key, value in params.items():
        if key in json:
            prediction_data.append(json[key])
        else:
            prediction_data.append(value)

    predictor = Predictor()

    prediction_data = pd.DataFrame([prediction_data])

    predictions = predictor.predict_model(prediction_data)

    return jsonify(predictions)


if __name__ == '__main__':
    app.run()

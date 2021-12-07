import pandas as pd
from flask import Flask, request, jsonify

import sensors
from predictor import Predictor

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def index():
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

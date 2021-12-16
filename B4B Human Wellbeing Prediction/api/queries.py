import os
import json
import sensors
import pandas as pd
from random import choice
import cloudpickle as pickle
from predictor import Predictor


def register(query):
    @query.field("predict")
    def predict_resolver(obj, info, input):
        prediction_data = {
            'temperature': (input["temperature"] if "temperature" in input else sensors.get_temperature()),
            'mean_temp_day': (input["mean_temp_day"] if "mean_temp_day" in input else sensors.get_mean_temp_day()),
            'heat_index': (input["heat_index"] if "heat_index" in input else sensors.get_heat_index()),
            'relative_humidity': (
                input["relative_humidity"]
                if "relative_humidity" in input
                else sensors.get_relative_humidity()
            ),
            'light_sensor_one_wave_length': (
                input["light_sensor_one_wave_length"]
                if "light_sensor_one_wave_length" in input
                else sensors.get_light_sensor_one_wave_length()
            ),
            'light_sensor_two_wave_length': (
                input["light_sensor_two_wave_length"]
                if "light_sensor_two_wave_length" in input
                else sensors.get_light_sensor_two_wave_length()
            ),
            'number_of_occupants': (
                input["number_of_occupants"]
                if "number_of_occupants" in input
                else sensors.get_number_of_occupants()
            ),
            'activity_of_occupants': (
                input["activity_of_occupants"]
                if "activity_of_occupants" in input
                else sensors.get_activity_of_occupants()
            ),
            'state_of_door': (
                (1 if input["state_of_door"] is True else 0)
                if "state_of_door" in input else sensors.get_state_of_door()
            ),
            'hour': (input["hour"] if "hour" in input else sensors.get_hour()),
            'minute': (input["minute"] if "minute" in input else sensors.get_minute()),
            'second': (input["second"] if "second" in input else sensors.get_second()),
            'window_state': (
                (1 if input["window_state"] is True else 0)
                if "window_state" in input else sensors.get_window_state()
            ),
            'room_A': ((1 if input["room"] == 0 else 0) if "room" in input else None),
            'room_B': ((1 if input["room"] == 1 else 0) if "room" in input else None),
            'room_C': ((1 if input["room"] == 2 else 0) if "room" in input else None),
            'relative_time': (input["relative_time"] if "relative_time" in input else sensors.get_relative_time()),
        }

        if (
                prediction_data["room_A"] is None
                and prediction_data["room_B"] is None
                and prediction_data["room_C"] is None
        ):
            # @TODO: Replace with sensors.get_room() ?
            prediction_data[f"room_{choice(['A', 'B', 'C'])}"] = 1

        predictor = Predictor()

        with open(f"{os.path.dirname(os.path.abspath(__file__))}/shap_data.pkl", "rb") as f:
            shap = pickle.load(f)

        prediction_df = pd.DataFrame([list(prediction_data.values())])

        return {

            "satisfaction": predictor.predict_model(prediction_df),
            "shapOptions": json.dumps({})  # .__dict__
        }

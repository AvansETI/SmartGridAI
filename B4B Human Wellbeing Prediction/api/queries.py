import json
import sensors
import pandas as pd
from random import choice
from predictor import Predictor
from utils import calculate_heat_index


def register(query):
    @query.field("predict")
    def predict_resolver(obj, info, input):
        """
        Resolver for the predict route, uses the input data and the sensors to create a parsable prediction data array, then uses the t-pot model to make a prediction.
        Args:
            input: Input dictionary from the client

        Returns:
            diciontary with the prediction and shap data
        """
        prediction_data = {
            "hour": (input["hour"] if "hour" in input else sensors.get_hour()),
            "minute": (input["minute"] if "minute" in input else sensors.get_minute()),
            "second": (input["second"] if "second" in input else sensors.get_second()),
            "relative_time": (
                input["relative_time"]
                if "relative_time" in input
                else sensors.get_relative_time()
            ),
            "temperature": (
                input["temperature"]
                if "temperature" in input
                else sensors.get_temperature()
            ),
            "mean_temp_day": (
                input["mean_temp_day"]
                if "mean_temp_day" in input
                else sensors.get_mean_temp_day()
            ),
            "heat_index": (
                input["heat_index"]
                if "heat_index" in input
                else (
                    calculate_heat_index(
                        input["temperature"], input["relative_humidity"]
                    )
                    if ("temperature" in input and "relative_humidity" in input)
                    else sensors.get_heat_index()
                )
            ),
            "relative_humidity": (
                input["relative_humidity"]
                if "relative_humidity" in input
                else sensors.get_relative_humidity()
            ),
            "light_sensor_one_wave_length": (
                input["light_sensor_one_wave_length"]
                if "light_sensor_one_wave_length" in input
                else sensors.get_light_sensor_one_wave_length()
            ),
            "light_sensor_two_wave_length": (
                input["light_sensor_two_wave_length"]
                if "light_sensor_two_wave_length" in input
                else sensors.get_light_sensor_two_wave_length()
            ),
            "number_of_occupants": (
                input["number_of_occupants"]
                if "number_of_occupants" in input
                else sensors.get_number_of_occupants()
            ),
            "activity_of_occupants": (
                input["activity_of_occupants"]
                if "activity_of_occupants" in input
                else sensors.get_activity_of_occupants()
            ),
            "state_of_door": (
                (1 if input["state_of_door"] is True else 0)
                if "state_of_door" in input
                else sensors.get_state_of_door()
            ),
            "window_state": (
                (1 if input["window_state"] is True else 0)
                if "window_state" in input
                else sensors.get_window_state()
            ),
            "room_A": ((1 if input["room"] == 0 else 0) if "room" in input else None),
            "room_B": ((1 if input["room"] == 1 else 0) if "room" in input else None),
            "room_C": ((1 if input["room"] == 2 else 0) if "room" in input else None),
        }

        if (
            prediction_data["room_A"] is None
            and prediction_data["room_B"] is None
            and prediction_data["room_C"] is None
        ):
            # @TODO: Replace with sensors.get_room() ?
            prediction_data[f"room_{choice(['A', 'B', 'C'])}"] = 1

        predictor = Predictor()

        prediction_df = pd.DataFrame([list(prediction_data.values())])
        return {
            **(predictor.predict_model_proba(prediction_df)),
            "shapOptions": json.dumps(predictor.plot(prediction_df).data),
        }

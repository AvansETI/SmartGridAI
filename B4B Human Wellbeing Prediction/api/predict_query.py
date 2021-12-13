import sensors
import pandas as pd
from predictor import Predictor


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
        'state_of_door': (input["state_of_door"] if "state_of_door" in input else sensors.get_state_of_door()),
        'hour': (input["hour"] if "hour" in input else sensors.get_hour()),
        'minute': (input["minute"] if "minute" in input else sensors.get_minute()),
        'second': (input["second"] if "second" in input else sensors.get_second()),
    }

    predictor = Predictor()
    prediction_df = pd.DataFrame([list(prediction_data.values())])

    return predictor.predict_model(prediction_df)

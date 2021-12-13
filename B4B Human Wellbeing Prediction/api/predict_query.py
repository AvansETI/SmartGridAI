import sensors
import pandas as pd
from predictor import Predictor


def predict_resolver(
    obj, info,
    temperature=None, mean_temp_day=None, heat_index=None, relative_humidity=None,
    light_sensor_one_wave_length=None, light_sensor_two_wave_length=None,
    number_of_occupants=None, activity_of_occupants=None, state_of_door=None,
    hour=None, minute=None, second=None
):
    try:

        prediction_data = {
            'temperature': temperature or sensors.get_temperature(),
            'mean_temp_day': mean_temp_day or sensors.get_mean_temp_day(),
            'heat_index': heat_index or sensors.get_heat_index(),
            'relative_humidity': relative_humidity or sensors.get_relative_humidity(),
            'light_sensor_one_wave_length': light_sensor_one_wave_length or sensors.get_light_sensor_one_wave_length(),
            'light_sensor_two_wave_length': light_sensor_two_wave_length or sensors.get_light_sensor_two_wave_length(),
            'number_of_occupants': number_of_occupants or sensors.get_number_of_occupants(),
            'activity_of_occupants': activity_of_occupants or sensors.get_activity_of_occupants(),
            'state_of_door': state_of_door or sensors.get_state_of_door(),
            'hour': hour or sensors.get_hour(),
            'minute': minute or sensors.get_minute(),
            'second': second or sensors.get_second(),
        }

        predictor = Predictor()
        prediction_df = pd.DataFrame([ list(prediction_data.values()) ])
        prediction = predictor.predict_model(prediction_df)

    except Exception as error:
        print(error)
        prediction = 0

    return prediction

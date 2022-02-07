# ETL Notes

## Requirements

Install the required packages (requirements.txt) \
The source datasets can be found at https://github.com/IoTsec/Room-Climate-Datasets \
Download those datasets and put them alongside the notebooks, the file structure should look as follows.

- Dataset
  - datasets-location_A
  - datasets-location_B
  - datasets-location_C

### Calculation

To calculate this satisfaction the standard specifies the acceptability limits, if someone falls within this upper and lower limit then they are satisfied.

The limit for 80% comfort is A thermal environment that a substantial majority(more than 80%) of the occupants find thermally acceptable.

Tpmaout is the prevailing mean outside temperature.

Upper limit 80% comfort = (0.31 _ tpmaout) + 21.3 \
Lower limit 80% comfort = (0.31 _ tpmaout) + 14.3

![Define the 80% limit](images/calculation2.jpeg)
_Calculation comfort limits_

This is the limit that determines where the lines are drawn on the ASHRAE 55 graph.
You then plot your mean outside temperature and inside temperature to define if someone falls between these limits, if they do then they're comfortable.

![Ashrae55 graph](images/Ashrea55.png)
_Ashrae 55 adaptive model graph_

## Used climate dataset explenation

When we determined that we couldn't get our own data we started looking for already existing studies which would satisfy our climate data requirements.
We found two potential sources for our data from previous studies.

- [Appliances energy prediction Data Set](https://archive.ics.uci.edu/ml/datasets/Appliances+energy+prediction)
- [Room climate dataset](https://github.com/IoTsec/Room-Climate-Datasets)

After assassing both datasets we found that the features off the room climate dataset better align with our data requirements.
We will use this as a dataset for our climate data to prove our hypothese.

## Human-satisfaction mock data creation

Now that we have our dataset and our mock creation standard we have to apply the ASHRAE55 standard on it to get our satisfaction data.
To do this we looked around for an already existing package so we don't have to implement the entire standard ourselves.
We found this package [Pythermalcomfort](https://pypi.org/project/pythermalcomfort/) which implements a bunch of thermal comfort standards, including the adpative model we will use.

We combined this package and the climate dataset to create the acceptability_80% feature for our dataset. The code for this can be found [here](https://github.com/AvansETI/SmartGridAI/blob/b4bux/development/B4B%20Human%20Wellbeing%20Prediction/data_gathering/transform.ipynb).

### Column details

- original_entry_id: Data is concatinated from multiple days/rooms, these are the original entry id's from those sources
- node_id: At what place in the room the data was collected from, [see floor plans section](#floor-plans)
- room: Which room was used, [see floor plans section](#floor-plans)
- absolute_time: Unix timestamp of reading
- relative_time: The time between this and the previous reading
- date: Date of reading
- temperature: Temperature in Celsius
- mean_temp_day: The mean temperature from the day of the reading in Mannheim Germany (place where the study took place)
- heatindex: What the temperature feels like
- relative_humidity: Percentage of humidity in the air
- light_sensor_one_wavelength: Wavelength in nm at reading time
- light_sensor_two_wavelength: Wavelength in nm at reading time
- number_occupants: Amount of people in the room at the time of the reading
- activity_occupants: Activity the occupants were doing at the time off the reading (0 = n/a, 1 = read, 2 = stand, 3 = walk, 4 = work)
- door_state: Was the door open or closed
- window_state: was the window open or closed
- tmp_cmf: Comfort temperature a that specific running mean temperature, in °C
- tmp_cmf_80_low: Lower acceptable comfort limit for 80% occupants, in °C
- tmp_cmf_80_up: Upper acceptable comfort limit for 80% occupants, in °C
- tmp_cmf_90_low: Lower acceptable comfort limit for 90% occupants, in °C
- tmp_cmf_90_up: Upper acceptable comfort limit for 90% occupants, in °C
- acceptability_80: Acceptability for 80% occupants
- acceptability_90: Acceptability for 90% occupants

# Figures

## Acceptability 80% distribution

![Acceptability 80% distribution](images/acceptability_80.png)
_Acceptability 80% distribution in our dataset_

## Acceptability 90% distribution

![Acceptability 90% distribution](images/acceptability_90.png)
_Acceptability 90% distribution in our dataset_

<h2 id="floor-plans">Floor plans dataset</h2>
<h3>Room A</h3>
<img src="images/room_a.png"/>
<h3>Room B</h3>
<img src="images/room_b.png"/>
<h3>Room C</h3>
<img src="images/room_c.png"/>

## Sources

- Study used as datasource: https://github.com/IoTsec/Room-Climate-Datasets

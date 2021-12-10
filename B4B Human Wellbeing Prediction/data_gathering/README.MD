# ETL Notes

## Requirements
Install the required packages (requirements.txt) \
The source datasets can be found at https://github.com/IoTsec/Room-Climate-Datasets \
Download those datasets and put them alongside the notebooks, the file structure should look as follows.

+ Dataset
    + datasets-location_A
    + datasets-location_B
    + datasets-location_C


## Column details
+ original_entry_id: Data is concatinated from multiple days/rooms, these are the original entry id's from those sources.
+ node_id: At what place in the room the data was collected from, [see floor plans section](#floor-plans) 
+ room: Which room was used, [see floor plans section](#floor-plans) 
+ absolute_time: Unix timestamp of reading
+ relative_time: The time between this and the previous reading
+ date: Date of reading
+ temperature: Temperature in Celsius
+ mean_temp_day: The mean temperature from the day of the reading in Mannheim Germany (place where the study took place)
+ heatindex: What the temperature feels like
+ relative_humidity: Percentage of humidity in the air
+ light_sensor_one_wavelength: Wavelength in nm at reading time
+ light_sensor_two_wavelength: Wavelength in nm at reading time
+ number_occupants: Amount of people in the room at the time of the reading
+ activity_occupants: Activity the occupants were doing at the time off the reading  (0 = n/a, 1 = read, 2 = stand, 3 = walk, 4 = work)
+ door_state: Was the door open or closed
+ window_state: was the window open or closed
+ tmp_cmf: Comfort temperature a that specific running mean temperature, in °C
+ tmp_cmf_80_low: Lower acceptable comfort temperature for 80% occupants, in °C
+ tmp_cmf_80_up: Upper acceptable comfort temperature for 80% occupants, in °C
+ tmp_cmf_90_low: Lower acceptable comfort temperature for 90% occupants, in °C
+ tmp_cmf_90_up: Upper acceptable comfort temperature for 90% occupants, in °C
+ acceptability_80: Acceptability for 80% occupants
+ acceptability_90: Acceptability for 90% occupants

## What we want from our dataset
We decided early on in the project that we would need to combine climate data from sensors placed inside a room, office, classroom with some kind of human satisfaction data, active feedback or passive feedback. 

### climate data requirements
For the climate data we would ideally get the following features.
+ temperature
+ humidity
+ IAQ data(indoor air quality)
+ doorstate
+ windowstate
+ room(if we use multiple rooms)
furthermore we would prefer our data to also be historical for the sake of model training.

#### where would this data come from
Through our meetings we have found out about a living lab(SENDlab) inside of Avans, after another follow-up meeting with Maurice Snoeren we came to the conclusion that the current SENDlab doesnt have our data requirements.\
At the same time we were looking at the SENDlab we had various contact points with our stakeholders about getting data from one off them.\
After our initial meeting we found out that strukton and Olivia potentially have a datasource for us, after sending out 4 emails with another follow-up email the week after to these stakeholders we've gotten no response.\
Because off this non-communication we decided to mock our dataset and future-proof our project so the next group that will pick it up will only have to exchange our mock dataset for the real one.

### satisfaction data requirements
Our project is focused on predicting user-satisfaction based on climate data with machine learning, thus we need some kinda of feedback from our users to train on.\
This feature would idealy be a yes or no on if that person is comfortable or not.\

To the satisfaction data we could either choose for active or passive feedback.\
Early on Erik Kluijtmans found an existing study detailing that passive feedback isn't yet ready to accommodate individual differences in thermal comfort.

A qoute from the study.
>Current methods of evaluating thermal comfort in buildings are unable to accommodate individual 
differences in thermal sensations and preferences due to their “one size fits all” approach.

#### our approach to active feedback
We started focusing our efforts to getting some kind of active feedback from the people inside the living lab. THere are a couple ways to get this data.
+ Create an app where students can leave feedback about their comfort.
+ Use moodboxes that students press when leaving a room, rating the comfort for that class.

After some discussion we came to the conclusion we would focus on the moodboxes because an app would.\

Why we don't want to use an app.
1. An app could be used to answer whenever they want during class or more than once, making it less generalised over the entire class.
2. An app could be used as a complain-app more than for actual feedback.

Why we want to use moodboxes.
1. We specify when and where someone gives feedback(at the end of class when they walk out).
2. Avans has a past record of using moodboxes so they could already be available to us.

##### getting the moodboxes.
We then started contacting concerned party at Avans who would know about these buttons. Through this we found out that the moodbox-campaign wasn't done by Avans itself but by a third party.\

To follow-up on this discovery we contacted this third party about potentially getting one or more moodboxes from them, we didn't get a reply from them after the initial email and after the follow-up email.\

After not getting a reply this way we discussed our moodboxes idea in the stakeholder meeting. There was potentially a space for us at strukton where we could place said buttons but getting the required compliance from strukton would take too long for our turn-around time.
## Why we dont use b4bux specific dataset
This basically left us without any real climate data or feedback data which is when we looked at some already existing thermal-comfort standards([ASHRAE 55 standard](https://www.researchgate.net/figure/ASHRAE-55-limits-for-thermal-Comfort-adapted-from-ASHRAE-55-2017_fig5_327597687), [publication 74](https://www.vabi.nl/wp-content/uploads/2016/02/Open-hier-Comforteisen-toetsen-met-gebouwsimulatie.pdf).\

### ASHREA 55 standard

## Climate dataset explenation

## Human-satisfaction mock data creation

Comfort data model based on the [ASHRAE 55 standard](https://www.researchgate.net/figure/ASHRAE-55-limits-for-thermal-Comfort-adapted-from-ASHRAE-55-2017_fig5_327597687), which is about the same as [pub 74](https://www.vabi.nl/wp-content/uploads/2016/02/Open-hier-Comforteisen-toetsen-met-gebouwsimulatie.pdf). 

## Acceptability 80% distribution
![Acceptability 80% distribution](images/acceptability_80.png)

## Acceptability 90% distribution
![Acceptability 90% distribution](images/acceptability_90.png)

<h2 id="floor-plans">Floor plans dataset</h2>
<h3>Room A</h3>
<img src="images/room_a.png"/>
<h3>Room B</h3>
<img src="images/room_b.png"/>
<h3>Room C</h3>
<img src="images/room_c.png"/>

## Sources
+ Study used as datasource: https://github.com/IoTsec/Room-Climate-Datasets

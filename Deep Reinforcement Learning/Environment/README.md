# Smart grid environment for reinforcement learning

The project "Becomes a smart grid with AI really smart?" has taken off within the applied research group
Smart Energy and Datascience & ICT of Avans Hogeschool (The Netherlands). Artificial intelligence is applied
to the smart energy playing field, to control a smart grid consisting of different type of power elements.
A smart grid could consist of solar panels, battery storage and consumers. It could be a very complex task
to become energy neutral. This project is going to experiment with deep reinforcement learning to see how
a AI would do the task to become energy neutral.

# Smart grid model

Currently, the smart grid model is focussed on electricity. Heat is another import aspect of the energy of 
a household. This could be embedded in a later stage. The smart grid model consists of five parts:
1. Storage
2. Production
3. Fixed or unplannable consumption (user decides)
4. Planned consumption (user has requirements)
5. User (playing a role to use appliances that consume electricity)

# Available grid model components

The grid model is implemented by smartgrid_env and uses all the available components if possible. This
environment used the API as defined by the OpenAI Gym structure.

1. Storage
    * battery_model (v0.1)
2. Production
    * solar_panel_model (v0.1)
    * solar_predication_model
    * weather_data_model
3. Fixed consumption
    * ...
4. Planned consumption
    * appliance_model (v0.2)
5. User
    * user_model

## Battery model

This battery model simulates the behavior of a battery with a certain capacity and maximum power charge and discharge rate.
The efficiency loss during the conversion of the charge and discharge is not taken into account. A set point is used to 
control the battery output to a certain level. When the capacity is insufficient, the power output will decrease automatically.
Currently the dynamic behavior of the battery is not taken into account. The model implements a simple straigthforward
bucket model that can be charges and discharged.

Future improvements:
* Take the efficiency into account of the battery
* Implement dynamic behavior of the battery
* Implementation of a real battery model (check Matlab Simulink)

Example:
```python
setup = {
    'capacity_initial_wh'   : 3500,
    'max_power_charge_w'    : 5 * 1000,
    'max_power_discharge_w' : 5 * 1000
}

battery = BatteryModel(setup)

for _ in range(10):
    battery.step(60*30, 10000) # Performs a timestep and calculates
    battery.print()
```

Console:
```
Battery: 0 W (3500Wh) - Setpoint: 0
Battery: 5000.0 W (1000.0Wh) - Setpoint: 10000
Battery: 2000.0 W (0Wh) - Setpoint: 10000
Battery: 0.0 W (0Wh) - Setpoint: 10000
Battery: 0.0 W (0Wh) - Setpoint: 10000
```

# Smart grid test environment (smartgrid_test_env.py)

## Description:
Smart grid environment that simulates a household for one year. This version is a first initial version to test the openai environment model.

## Observation: 
Type: Box(6)
Num	Observation                     Min         Max
0   Grid [Wh]                       0           Inf
1	Solar Enery [Wh]                0           Inf
2   Battery Energy [Wh]             -Inf        Inf
3   Battery Current Capacity [Wh]   0           Inf
4   Consumption power [W]           0           Inf
5   Time [s] 1/1 - 31/12            0           31622400 

NOTE: Consumption not implemented and zero is returned

## Actions:
Type: Box(1)
Num	Action                      Min         Max
0	Battery Set Point           -cap_W      +cap_W
        
## Reward:
Reward is the difference of the sum (of each step) of solar power + battery power and consumption.
Reward = sum(Solar Power) + sum(Battery) - sum(Consumption)
Reward range -Inf to Inf

## Starting State:
Observations start at zero.

## Episode Termination:
After one year.
Later: When the power grid is used!

Apply the reward functions so the system will learn when it is making the right decisions. we will try each of them separately from another to see which gets the highest reward and works best.

1. Define parameters:
* P_production = The power that is produced within the solar cells
* P_storage = Power that is used from the battery
* P_consumption = A combination of power which we can and cannot influence on when it will be used.
* E_storage = Energy that is stored in the battery
* E_storage_max = The maximum capacity of energy stored in the battery
* P_facility = The power used of a power supplier

P_facility = P_consumption - P_production - P_storage
So the power used of the power supplier is the total of power consumed minus what is produced by the solar cells minus what is stored on the battery.

#  Reward function 1
R_power = Σ(-P_facility)
(Game over = Σ(P_facility) > 0)
(Game over if t > t_deadline)
Reward = R_power

The goal is using only using power that is self obtained. Therefore P_facility would be a negative number because the system needs to save energy. The reward would be the total of this energy saved. 
The system needs to stop when he uses energy from the power supplier or when the system does not meet one of the user's deadlines. This will be in every test.


#  Reward function 2
R_energy = Σ(E_storage / E_storage_max)
R2 = R_power + a * R_energy
(Game over = Σ(P_facility) > 0)
(Game over if t > t_deadline) 

The second reward function adds the stage of the battery. Because the number for R_energy will always be in a range from 0 to 1. Multiplying this value with a undetermined value will increase the reward, therefore it becomes interesting for the system to take the stage of the battery into account.


#  Reward function3
R_happiness = Σ(n_completed_deadlines / n_deadlines)
R3 = R_power + a * R_happiness
(Game over = Σ(P_facility) > 0)


The third function is similar to function 2 but instead of using the battery stage we add user happiness. The user sets his demands, for example he wants his laundry be done before the end of the weekend and the dishes be done by 8 p.m. 

#  Reward function 4
R4 =  R_power + a * R_energy + b * R_happiness
(Game over = Σ(P_facility) > 0)


The last test function uses all three the ways to reward the system.
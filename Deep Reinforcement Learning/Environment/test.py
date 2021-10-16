import os
from battery_model import BatteryModel
#from washing_machine_model import WashingMachineModel
from time_serie_reader import TimeSerieReader
from solar_panel_model import SolarPanelModel

from smartgrid_test_env import SmartgridTestEnv

sg = SmartgridTestEnv()
for i in range(0, 100):
    action = [10]#sg.action_space.sample()
    observation, reward, done, info = sg.step(action)
    print(reward)

#sp = SolarPanelModel({})
#sum = 0
#for i in range(0, 2*3600*24, 100):
#    diff_wh = sp.step(i)
#    sum = sum + diff_wh
#    print( str(i) + ": " + str(diff_wh) + ": " + str(sum) )

#file = os.path.dirname(os.path.realpath(__file__)) + "\\data\\test-data.csv"
#print("file: " + file)

#tsr = TimeSerieReader(file)
#tsr = TimeSerieReader("data/test-data.csv")
#tsr = TimeSerieReader("data/washing_machine_30_degrees_celsius_program.csv")

#for i in range(0, 10000, 100):
#    print(str(tsr.interpolate(i)))
#    if ( tsr.reached_end ):
#        print ("YEAD")



#wm = WashingMachineModel({})


#wm.start()
#for i in range(1000):
#print(wm.step(70))
#print(wm.step(70))
#print(wm.step(70))


#battery = BatteryModel({'capacity_initial_wh': 3500})
#battery.print()

#for _ in range(10):
#    battery.step(60*30, 10000)
#    battery.print()

# for _ in range(20):
#     battery.step(60*30, -7000)
#     battery.print()

# wmm = WashingMachineModel({})
# wmm.start()
# wmm.print()

# for _ in range(10):
#     wmm.step(60)
#     wmm.print()

# for _ in range(20):
#     wmm.step(60*30)
#     wmm.print()


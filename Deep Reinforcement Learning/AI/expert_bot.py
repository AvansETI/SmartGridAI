import numpy as np

class ExpertBot:
    def calc_action(self, observation):
        _, solar_wh, _, _, consumption_wh, _, = observation
        batSetpoint = [0]
        if (solar_wh > consumption_wh):
            batSetpoint[0] = -np.inf
        elif (solar_wh < consumption_wh):
            batSetpoint[0] = np.inf
        return batSetpoint
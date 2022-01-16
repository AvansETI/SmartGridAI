import heat_index


def calculate_heat_index(temperature, relative_humidity):
    return heat_index.calculate.from_celsius(temperature, relative_humidity)

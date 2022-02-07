import heat_index


def calculate_heat_index(temperature, relative_humidity):
    """
    Calls the heat index package and
    Args:
        temperature: Current temperature
        relative_humidity: De relative humidity on a scale from 0.00 to 1.00

    Returns:
        The heat index value
    """
    return heat_index.calculate.from_celsius(temperature, relative_humidity)

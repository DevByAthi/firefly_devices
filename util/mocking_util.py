from typing import Tuple


def generate_actuator_message_text(lat: float, long: float, acc: Tuple[float, float, float],
                                   gyro: Tuple[float, float, float], mag: Tuple[float, float, float], baro: float,
                                   altitude: float, temp: float):
    """

    :param lat:
    :param long:
    :param acc:
    :param gyro:
    :param mag:
    :param baro:
    :param altitude:
    :param temp:
    :return:
    """
    d = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lat, long]
        },
        "properties": {
            "device_type": 'actuator',
            "temperature": {
                "value": temp,
                "unit": "celcius"
            },
            "baro": {
                "value": baro,
                "unit": "mBar"
            },
            "altitude": {
                "value": altitude,
                "unit": "m"
            },
            "acc": {
                "x": acc[0],
                "y": acc[1],
                "z": acc[2]
            },
            "gyro": {
                "x": gyro[0],
                "y": gyro[1],
                "z": gyro[2]
            },
            "mag": {
                "x": mag[0],
                "y": mag[1],
                "z": mag[2]
            }
        }
    }
    return str(d).replace("'", '"')


def generate_sensor_message_text(lat, long, temp, hum, co, pm):
    """
    Generates message string by creating a temporary dictionary object and substituting given values in
    :param lat:
    :param long:
    :param temp:
    :param hum:
    :param co:
    :param pm:
    :return:
    """
    d = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lat, long]
        },
        "properties": {
            "device_type": 'sensor',
            "temperature": {
                "value": temp,
                "unit": "celcius"
            },
            "humidity": {
                "value": hum,
                "unit": "%"
            },
            "carbon_monoxide": {
                "value": co,
                "unit": "ppm"
            },
            "pm2_5": {
                "value": pm,
                "unit": "ppm"
            }
        }
    }
    return str(d).replace("'", '"')

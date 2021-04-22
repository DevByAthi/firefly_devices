# COPIED FROM https://github.com/Azure-Samples/azure-iot-samples-python/blob/master/iot-hub/Quickstarts/simulated-device/SimulatedDevice.py

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import dotenv

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

config = dotenv.dotenv_values()

# The device connection string to authenticate the device with your IoT hub.
DEVICE_CONNECTION_STRING = config['DEVICE_CONNECTION_STRING']

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
CARBON_MONOXIDE = 10
MSG_TXT = '{{"type": "Feature", "geometry" : {{"type" : "Point", "coordinates" : {coords}}}, "properties" : {{ "device_type" : "{device_type}", "temperature" : {{"value" : "{temperature}", "unit" : "celcius"}}, "humidity" : {{"value" : "{humidity}", "unit" : "celcius"}}, "CO" : {{"value" : "{carbon_monoxide}", "unit" : "ppm"}}}}}}'


# MSG_TXT = '{{"temperature" : {{"value" : "{temperature}", "unit" : "celcius"}}, "humidity" : {{"value" : "{humidity}", "unit" : "celcius"}}, "CO" : {{"value" : "{carbon_monoxide}", "unit" : "celcius"}}}}'


def generate_message_text(lat, long, device_type, temp, hum, co, pm):
    d = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lat, long]
        },
        "properties": {
            "device_type": device_type,
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


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)
    return client


def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        while True:
            # Build the message with simulated telemetry values.
            device_type = 'actuator'
            coordinates = [28.5, -34.7]
            temperature = TEMPERATURE + (random.random() * 15)
            humidity = HUMIDITY + (random.random() * 20)
            carbon_monoxide = CARBON_MONOXIDE + ((random.random() - 0.5) * 10)
            msg_txt_formatted = MSG_TXT.format(device_type=device_type, temperature=temperature, humidity=humidity,
                                               carbon_monoxide=carbon_monoxide, coords=coordinates)
            message = Message(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            if temperature > 30:
                message.custom_properties["temperatureAlert"] = "true"
            else:
                message.custom_properties["temperatureAlert"] = "false"

            # Send the message.
            print("Sending message: {}".format(message))
            client.send_message(message)
            print("Message successfully sent")
            time.sleep(1)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")


if __name__ == '__main__':
    print("IoT Hub Quickstart #1 - Simulated device")
    print("Press Ctrl-C to exit")
    iothub_client_telemetry_sample_run()

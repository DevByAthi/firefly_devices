"""

This program simulates sensor readings being sent to the IoT Hub. Must have an Azure subscription with an IoT Hub instance defined.

NOTE: This draws heavily from https://github.com/Azure-Samples/azure-iot-samples-python/blob/master/iot-hub/Quickstarts/simulated-device/SimulatedDevice.py

by Athreya Murali
"""

# COPIED FROM

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import threading
import time
import dotenv

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import geojson
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

from util.mocking_util import generate_actuator_message_text
from util.status import Status

config = dotenv.dotenv_values()

# The device connection string to authenticate the device with your IoT hub.
DEVICE_CONNECTION_STRING = config['DEVICE_CONNECTION_STRING']

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
BAROMETRIC_PRESSURE = 1013.25
ALTITUDE = 50
HUMIDITY = 60
CARBON_MONOXIDE = 10

METHOD_NAME = "DetermineFlightPath"
STATUS = Status.IDLE


def device_method_listener(device_client):
    global STATUS
    while STATUS == Status.IDLE:
        method_request = device_client.receive_method_request()
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )
        if method_request.name == METHOD_NAME:
            print(method_request.payload)
            response_payload = {"Response" : "Successfully Received Coordinates. ACK"}
            response_status = 200
            STATUS = Status.FLYING
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        device_client.send_method_response(method_response)


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)
    return client


def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        # Start a thread to listen
        device_method_thread = threading.Thread(target=device_method_listener, args=(client,))
        device_method_thread.daemon = True
        device_method_thread.start()

        while True:
            if STATUS == Status.IDLE:
                # Build the message with simulated telemetry values.
                lat, long = 28.5, -34.7
                temperature = TEMPERATURE + (random.random() * 15)
                baro = BAROMETRIC_PRESSURE + ((random.random() - 0.5) * 60)
                altitude = ALTITUDE + ((random.random() - 0.5) * 12)
                acc = (random.random() * 2.0, random.random() * 2.0, random.random() * 2.0)
                gyro = (random.random() * 2.0, random.random() * 2.0, random.random() * 2.0)
                mag = (random.random() * 2.0, random.random() * 2.0, random.random() * 2.0)

                msg_txt_formatted = generate_actuator_message_text(lat, long, acc, gyro, mag, baro, altitude, temperature)
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

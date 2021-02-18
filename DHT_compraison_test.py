# SPDX-FileCopyrightText: 2021 Jose David Montoya
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
pin = board.D17
dhtDevice = adafruit_dht.DHT11(pin, use_pulseio=False)

# This code is use to test the Adafruit_Circuitpython_DHT library changin
# The values of the initialization times according to the DHT standard
# Found in some sources in the interweb



for i in range(755):
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    print(f"Cycle: {i}--Checksum Errors: {dhtDevice.checksum_test}--Data Buffer Error: {dhtDevice.data_buffer_test}"
          f"--Wiring Error: {dhtDevice.wiring_test}--Unknown Error: {dhtDevice.unplausible_test}")
    time.sleep(10.0)
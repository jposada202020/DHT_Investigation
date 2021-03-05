import time
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
pin = board.D18
dhtDevice = adafruit_dht.DHT11(pin, use_pulseio=False)

for i in range(10):
    try:
        dhtDevice = adafruit_dht2.DHT11(pin, use_pulseio=False)
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    time.sleep(5.0)
    dhtDevice.exit()

This is to document my own tests conducted on the ADAFRUIT_CIRCUITPYTHON_DHT library
I review the issues (open/closed) in the library. 

|Symptom  |Result   | 
|---|---|
|Unable to set line 4 to input' a   |killing any 'libgpiod_pulsein libgpiod_pulsein ( pgrep libgpiod_pulsein forexample ) and kill <PID found> did the trick. | 
|Using GPIO4 Does not work         |   Try disable 1-wire interface from raspi-config when using gpio4 with adafruit python lib.       |
|Using GPIO4 Does not work  | Change a to aifferent Pin. Some poeple report D17 working   | 
|New library does not work  |A Lot of people reports that old library works fine https://github.com/adafruit/Adafruit_Python_DHT  |
|A full buffer was not returned. Try again. and less frequently Checksum did not validate.        |           |
|ValueError: Object has been deinitialized and can no longer be used. Create a new object.        |           |
|Ubuntu 20.04/Raspberry Pi OS 10 64-bits on my RPi 4B, and the libgpiod_pulsein library shipped with adrafruit_blinka Python package is 32-bits.        |Recompile libgpiod library for the 64 platform           |
|Running: Adafruit CircuitPython 6.0.1 on 2020-12-28; FeatherS2 with ESP32S2        |           |
|DHT22 reports wrong negative temperatures         |           |
|DHT22 not working on Raspberry Pi Pico using CircuitPython        |           |
|sudo apt-get install libgpiod2 fails Unable to locate package libgpiod2|upgrade to buster|
|make sure your user is part of 'gpio' group.||

Some people recommend using the old adafruit-python-dht library, so I decide to take at look.. why the old library worked for some people?
To be clear here we are talking about Bitbanging and note PULSEIN.

I found that the new library uses the following code to start the communication

        dhtpin.direction = Direction.OUTPUT
        dhtpin.value = True
        time.sleep(0.1)
        dhtpin.value = False
        time.sleep(0.001)

However reviewing the odl library in C code I found that the initialization time were


      // Set pin high for ~500 milliseconds.
      pi_2_mmio_set_high(pin);
      sleep_milliseconds(500);
    
      // The next calls are timing critical and care should be taken
      // to ensure no unnecssary work is done below.
    
      // Set pin low for ~20 milliseconds.
      pi_2_mmio_set_low(pin);
      busy_wait_milliseconds(20);

I forked the library and did some test with the DHT11 adn DHT22 temperature sensor
I changed the Initialization values in the new library with the old ones, according to the OLD library. 
Test code is in this directory. I did this because I was unable to read my DHT11 with the times in the new library

Basically the code will test the sensor every 10 seconds for 750 cycles and will count where in the bitbanging
algorithm is an error.  I test this in the command line to avoid any overhead.

### DHT11

| |  | Machine | |
|:---:|:--------:|:-----:|:---:| 
| OS     |RP4    |RP3               |Zero W    |
|Stretch|N/A |Checksum Errors: 26<br/>Data Buffer Error: 198 <br />Wiring Error: 0<br />Unknown Error: 0|Checksum Errors: 0 <br />Data Buffer Error: 750<br />Wiring Error: 0<br />Unknown Error: 0 |
|Buster|Checksum Errors: 101<br/>Data Buffer Error: 1<br />Wiring Error: 0<br />Unknown Error: 0|Checksum Errors: 101 <br />Data Buffer Error: 30<br />Wiring Error: 0<br />Unknown Error: 0 |Checksum Errors: 0<br/>Data Buffer Error: 598<br />Wiring Error: 152<br />Unknown Error: 0|Checksum Errors: 0 <br />Data Buffer Error: 750<br />Wiring Error: 0<br />Unknown Error: 0 |


### DHT22

|      | |Machine                    |                            |
|---------|:----:|:-------------------------:|:--------------------------:|
|OS          |RP4 |RP3                        |Zero W                      |
|Stretch  |N/A  |Checksum Errors: 30<br/> Data Buffer Error: 200<br/>    Wiring Error: 0<br />  Unknown Error: 0  |Checksum Errors: 0<br/> Data Buffer Error: 0<br/> Wiring Error: 750<br/>                                        Unknown Error: 0          |
|Buster   |Checksum Errors: 110<br/> Data Buffer Error: 9<br/> Wiring Error: 0<br/> Unknown Error: 0|Checksum Errors: 86<br/> Data Buffer Error: 80<br/> Wiring Error: 0<br/> Unknown Error: 1|Checksum Errors: 0<br/>    Data Buffer Error: 749<br/>   Wiring Error: 1<br/>  Unknown Error: 0|


## Thoughts
There were not intensive testing, and for the money I will always select another Temperature Sensor. However, I start this electronics journey like many people with a KIT, and this kit include a DHT11 temperature sensor. Like me,
maybe there is some people that have this same journey. I remember porting the DHT11 BitBANG library from Arduino to Python, it was.. lets sy it was. That is why this little blue friend will always have a place in mi test JIG nad in my electronics box.
Now, technical data, according what I saw, the reliability of the measurements depends on both the Version of the RP used and the version
of the OS used.  The better the RP and the newer the OS, tthe better the reliability.

I submit a PR to change the logic in the library to take in account the difference in the trigger time for both sensors

In a last note. I did test the DHT22 sensor in negative temperatures.

There other code to for the bitbang if you like to test.

Have fun! Always!
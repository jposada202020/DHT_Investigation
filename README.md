This is to document my own tests conducted on the ADAFRUIT_CIRCUITPYTHON_DHT library
I review the issues (open/closed). Just verifying the behaviour of the DHT sensor with some RP models
compile a table that is in my REPO. link included

Some people recommend using the old adafruit-python-dht library, so I decide to take at look why the old library worked for some people
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
Test code is in the examples' directory
https://github.com/jposada202020/Adafruit_CircuitPython_DHT/blob/master/examples/dht_comparaison_test.py

Basically the code will test the sensor every 10 for 750 times and will count where in the bitbanging
algorithm we found the error.  I test this in the command line to avoid any overhead.

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
There were not intensive testing, and for the money I always select another Temperature Sensor. However, I start this electronics journey like many people with a KIT, and hit skit include a DHT11. Like me
maybe there is some people that have this. I remember porting the BitBANG library from Arduino to Python. That is why this little blue friend will always have a place in mi test JIG.
Now, technical data, according what I saw, the reliability of the measurements depends on both the Version of the RP used and the version
of the OS used.  The better the RP and the newer the OS, the reliability on the readings will improve.

If you happen to find this, just change the values as shown in my fork, and you could expect the above reliability if you want to use the DHT sensors

In a last note. I did not test the sensor in negative temperatures. you are more than welcome to do it

Have fun! Always!
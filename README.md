This is to document some test conducted on the ADAFRUIT_CIRCUITPYTHON_DHT library
I review the issues (open/closed). Just veryfing the behaviour of the DHT sensor with some RP models
compile a table that is in my REPO. link included

Some people recommend to use the old adafruit-python-dht library, so I decide to take at look why the old library worked for some people
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

Some tests done so far using a DHT11 with the new values according to the OLD library. Test code is 
in the examples directory

** DHT11
|OS  |Machine   | |
|----|----------|---|
|  |RP3               |Zero W    |
|Stretch  |Checksum Errors: 26  <br />Data Buffer Error: 198 <br />Wiring Error: 0<br />Unknown Error: 0|Checksum Errors: 0 <br />Data Buffer Error: 598<br />Wiring Error: 152<br />Unknown Error: 0 |
|Buster  |Checksum Errors: 101  <br />Data Buffer Error: 30 <br />Wiring Error: 0<br />Unknown Error: 0|Checksum Errors: 0 <br />Data Buffer Error: 750<br />Wiring Error: 0<br />Unknown Error: 0 |

** DHT22
|OS  |Machine   | |
|----|----------|---|
|  |RP3               |Zero W    |
|Stretch  |Checksum Errors: 30  <br />Data Buffer Error: 200 <br />Wiring Error: 0<br />Unknown Error: 0|Checksum Errors: TBT <br />Data Buffer Error: TBT<br />Wiring Error: TBT<br />Unknown Error: TBT |
|Buster  |Checksum Errors: TBT  <br />Data Buffer Error: TBT <br />Wiring Error: TBT<br />Unknown Error: TBT|Checksum Errors: TBT <br />Data Buffer Error: TBT<br />Wiring Error: TBT<br />Unknown Error: TBT |

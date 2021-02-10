Hello, sorry if this is not the correct channel butI do not know where to put or ask question regarding the libraries.
If was looking in some issues for the library
Adafruit_Circuitpython_DHT.
I review the issues (open/closed). I compile a table that is in my REPO. link included

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

So, I decide to compare the old with the new library, and here I am talking for the BITBANG as a lot of people raising the issues are using RPs

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

This times coincides with some standard found in ocfreaks.com and in sgbotic.com
Images attached.
I did some tests, altough not perfect, at least my DHT11 worked with the bitbang of the 
Adafruit_Circuitpython_DHT library 70% of the time

Last thing, I did find a sparkfun datasheet that mentions 1 ms as low signal to start listening,

Do anybody knows why we use 0.001 for the low signal? I really appreciate some insight. THANKS :)
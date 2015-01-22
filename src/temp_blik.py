#!/usr/bin/python

import time
import datetime
import sys
from pymlab import config

#### Script Arguments ###############################################

if len(sys.argv) != 2:
    sys.stderr.write("Invalid number of arguments.\n")
    sys.stderr.write("Usage: %s PORT ADDRESS\n" % (sys.argv[0], ))
    sys.exit(1)

port    = eval(sys.argv[1])

#### Sensor Configuration ###########################################

cfg = config.Config(
    i2c = {
            "port": port,
    },
    bus = [
        {
            "name":          "sht25",
            "type":        "sht25",
        },
         { "name":"gpio", "type":"I2CIO_TCA9535"},
    ],
)
cfg.initialize()

print "SHT25 humidity and temperature sensor example \r\n"
print "Temperature  Humidity[%%]  \r\n"
sht_sensor = cfg.get_device("sht25")
time.sleep(0.5)

i=0

#### Data ###################################################

gpio = cfg.get_device("gpio")


STATE_INIT = 0
STATE_TIMER_START = 1
STATE_TIMER_WAIT = 2
STATE_TIMER_NTH = 3
state = STATE_INIT


    
gpio.config_ports(0x0000, 0x0000)
gpio.set_ports(0b0)

while True:
    temperature = sht_sensor.get_temp();
    humidity = sht_sensor.get_hum();
   

    
    if state == STATE_INIT:
        gpio.set_ports(0b0)
        if temperature > 23:
            state = STATE_TIMER_START

    elif state == STATE_TIMER_START:
        gpio.set_ports(0b1001)
        t = time.time()
       # if temperature <= 23:
        #    state = STATE_INIT
        #else:
        state = STATE_TIMER_WAIT

    elif state == STATE_TIMER_WAIT:
        #gpio.set_ports(0b0110)
        if (time.time() - t) > 4:
            state = STATE_TIMER_NTH

    elif state == STATE_TIMER_NTH:
        gpio.set_ports(0b0)
        if temperature >23:
            state = STATE_TIMER_NTH
        else:
            state = STATE_INIT


    print "Temp: %.2f Hum: %.2f" % (temperature, humidity)
    time.sleep(1)
       



import pycom
from machine import UART
from machine import Pin
from machine import SD
from machine import RTC
import machine
import os
import time
# import logging
from L76GNSS import L76GNSS
from pytrack import Pytrack

py = Pytrack()
l76 = L76GNSS(py, timeout=30)

pycom.heartbeat(False)
uart = UART(0, baudrate=115200)
os.dupterm(uart)
rtc = RTC()

sd = SD()
os.mount(sd, '/sd')

# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger("test")
# log.debug("Test message: %d(%s)", 100, "foobar")

#Read the button, if pressed then not in deepsleep mode and connected to your wifi (to avoid many problem to update your code)
bouton = Pin('G4',mode=Pin.IN,pull=Pin.PULL_UP)
if bouton() == 0 or True: #TODO
    pycom.rgbled(0xff9900) #orange
    from network import WLAN
    wlan = WLAN(mode=WLAN.STA)
    nets = wlan.scan()
    for net in nets:
        if net.ssid == 'TP-LINK_2.4GHz':
            print('SSID present.')
            wlan.connect(net.ssid, auth=(net.sec, 'werbrauchtschoninternet'), timeout=5000)
            while not wlan.isconnected():
                machine.idle()
            print('Connetion WLAN/WiFi OK!')

            print("Sync time.")
            rtc.ntp_sync("pool.ntp.org")
            while not rtc.synced():
                print("Wait to be in sync")
                time.sleep(10)
            print("RTC is in sync. ",rtc.now())
            # machine.main('main2.py')
            # machine.main('main.py')
            break
else:
    pycom.rgbled(0x7f0000)
    # machine.main('main.py')
machine.main('main.py')

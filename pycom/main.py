# print("deepsleep prog")

from network import LoRa
import socket
import binascii
import struct
import time
import utime #utime
import pycom

init_timer = time.time()

sd_mounted = False
log_str = "\nInfo: {}\nBattery voltage: {}\nLocaltime: {}\nUptime: {}\n".format(os.uname(),py.read_battery_voltage(),utime.localtime(),utime.time())
if 'sd' in os.listdir('/'):
    print("SD-Card is mounted to /sd")
    sd_mounted = True
    log_file = open('/sd/log.txt', 'a')
    log_file.write(log_str)
    log_file.close()
else:
    print("No SD-Card mounted to /sd")
    print(log_str)


# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# Set network keys
app_eui = binascii.unhexlify('70B3D57ED0011B96')
app_key = binascii.unhexlify('68AD9E6FFF04548CB6EB6B50E60C00CC')


# create an ABP authentication params , use your own !
# dev_addr = struct.unpack(">l", binascii.unhexlify('260114F9'.replace(' ','')))[0] #replace 00 00 00 00
# nwk_swkey = binascii.unhexlify('EEEBE2155D1F711FA7ABF0A5CAA0BD80')  #replace 00000000000000000000000000000000
# app_swkey = binascii.unhexlify('7DBB921FAACF97752621D80D5C86076D') #replace 00000000000000000000000000000000

print("start join LoRa")
print(utime.localtime())#utime
print(utime.time())#utime
# join a network using ABP (Activation By Personalization)
# lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

#DEV EUI
print('Initializing LoRaWAN (OTAA), DEV EUI: {} ...'.format(
        binascii.hexlify(lora.mac()).decode('ascii').upper()))
# Join the network
print('Start Join')
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=0)
print('Wait for timeout')
pycom.rgbled(0xff0000)

# Loop until joined
while not lora.has_joined():
    print('Not joined yet...')
    pycom.rgbled(0x000000)
    time.sleep(0.1)
    pycom.rgbled(0xff0000)
    time.sleep(10)

print('Joined')
pycom.rgbled(0x0000ff)



# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
# lora.nvram_restore() #strange place for the restore but working.

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

while(True):
    print("Battery voltage: ",py.read_battery_voltage())
    print("Get coordinates")
    # save the coordinates in a new variable
    coord = l76.coordinates()
    # verify the coordinates received
    if coord == (None,  None):
        print("Retry getting coordinates...")
        pycom.rgbled(0x7f7f00)
        print('Uptime: ',utime.time())#utime
        continue
    print(coord)

    if sd_mounted:
        log_str = "{};{};{};{}\n".format(utime.localtime(),utime.time(),py.read_battery_voltage(),coord)

        log_file = open('/sd/log.txt', 'a')
        log_file.write(log_str)
        log_file.close()


    # send the Coordinates to LoRA
    print("sending")
    pycom.rgbled(0x0000ff) #bleu
    s.send(struct.pack("<i",  int(coord[0]*100000))+struct.pack("<i",  int(coord[1]*100000))+struct.pack("<H",  int(utime.time()))+struct.pack("<i",  int(py.read_battery_voltage()*1000000)))
    time.sleep(1)

    # lora.nvram_save() #nvram

    print("sent")
    print(time.time())
    print(utime.localtime())#utime
    print(utime.time())#utime
    pycom.rgbled(0x000000)
    #sleep
    print("sleep")

    time.sleep(180)
    # py.setup_sleep(180)
    # py.go_to_sleep()

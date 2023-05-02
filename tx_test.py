from functions import *
from pyrf24 import RF24

radio = RF24(22, 0)

if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

radio.setPALevel(2,1)
radio.setRetries(10,15)
radio.openWritingPipe(12345)
radio.channel = 50
radio.setPayloadSize(struct.calcsize("<B31s"))
radio.print_pretty_details()

payload = frament_the_text(compress(open_txt()))

ok = tx(payload)

#encendre leds en funció del valor de "ok"
#if ok:
#    continue
    #encendre un led
#elif not ok:
#    continue
    #encendre un altre led

radio.power = False

print("ok!")

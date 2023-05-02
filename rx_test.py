from functions import *
from pyrf24 import RF24

radio = RF24(22, 0)

if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

radio_setup(12345, True)

reception = rx()

#encendre leds en funció del valor de "reception[0]"
#if reception[0]:
#    continue
    #encendre un led
#elif not reception[0]:
#    continue
    #encendre un altre led

write(reception[1])

radio.power = False

print(reception[1])

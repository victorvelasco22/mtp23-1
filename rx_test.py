from functions import *
from pyrf24 import RF24

radioSetupRX()

reception = rx()

#encendre leds en funció del valor de "reception[0]"
#if reception[0]:
#    continue
    #encendre un led
#elif not reception[0]:
#    continue
    #encendre un altre led

write(reception[1])

radioPowerOff()

print(reception[1])
print("ok!")

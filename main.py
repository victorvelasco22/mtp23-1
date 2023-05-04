import RPi.GPIO as GPIO #importem la llibreria correpsonent
from functions import *
from pyrf24 import RF24
from time import sleep

radio = RF24(22, 0)

GPIO.setmode(GPIO.BCM) #establim com es fara referencia als pins de la RPi

#establim com es fara referencia als pins de la RPi
SW1=13 #active/stand by
SW2=19 #tx/rx
SW3=26 #fm/nm
SW4=21 
SW5=20 #write usb
SW6=16 #go/stop
SW7=12 #read usb


L_vermell=2 #active
L2=3 #rx if L2 & L3 NM
L3=27 #tx if L2 & L3 NM
L4=24 #write usb
L5=23 #read usb


#establim els pins conectats als switches com a inputs
GPIO.setup(SW1, GPIO.IN)
GPIO.setup(SW2, GPIO.IN)
GPIO.setup(SW3, GPIO.IN)
GPIO.setup(SW4, GPIO.IN)
GPIO.setup(SW5, GPIO.IN)
GPIO.setup(SW6, GPIO.IN)
GPIO.setup(SW7, GPIO.IN)

#tots els leds apagats al iniciar el programa
GPIO.output(L_vermell, GPIO.LOW)
GPIO.output(L2, GPIO.LOW)
GPIO.output(L3, GPIO.LOW)
GPIO.output(L4, GPIO.LOW)
GPIO.output(L5, GPIO.LOW)

#definicio dels diferents estats necesaris per a fer el main.
def active():
    while (GPIO.input(SW1)==True):
        if (GPIO.input(SW7)==True):
            led_manager(L_vermell,Off)
            read_usb()
            led_manager(L_vermell,On)
        elif (GPIO.input(SW5)==True):
            led_manager(L_vermell,Off)
            write_usb()
            led_manager(L_vermell,On)
        elif (GPIO.input(SW6)==True and GPIO.input(SW3)==True):
            led_manager(L_vermell,Off)
            network_mode()
            led_manager(L_vermell,On)
        elif (GPIO.input(SW6)==True and GPIO.input(SW3)==False and GPIO.input(SW2)==False):
            led_manager(L_vermell,Off)
            rx_mode()
            led_manager(L_vermell,On)
        elif (GPIO.input(SW6)==True and GPIO.input(SW3)==False and GPIO.input(SW2)==True):
            led_manager(L_vermell,Off)
            tx_mode()
            led_manager(L_vermell,On)
    
def read_usb():
    #AQUI cridar les funcions necesaries per a llegir del usb
    led_manager(L5,On)
    download_from_usb()
    while (GPIO.input(SW7)==True):
        continue
    led_manager(L5,Off)

def write_usb():
    led_manager(L4,On)

    #AQUI cridar les funcions necesaries per a escriure al usb
    upload_to_usb()
    while (GPIO.input(SW5)==True):
        continue
    led_manager(L4,Off)

def network_mode():
    led_manager(L2,On)
    led_manager(L3,On)

    #AQUI cridar les funcions necesaries per a executar el network mode
    while (GPIO.input(SW6)==True):
        continue
    led_manager(L2,Off)
    led_manager(L3,Off)

def tx_mode():
    led_manager(L3,On)
    #AQUI cridar les funcions necesaries per a executar el tx mode
    #radio = RF24(22, 0)

    #if not radio.begin():
    #    raise OSError("nRF24L01 hardware isn't responding")

    #radio_setup(12345, False)
    radioSetupTX()
    
    payload = frament_the_text(compress(open_txt()))

    ok = tx(payload)

    #encendre leds en funció del valor de "ok"
#    if ok:
#        print("OK")
#        #encendre un led
#    elif not ok:
#        print("NOT OK")
#        #encendre un altre led

    radio.power = False
    
    while (GPIO.input(SW6)==True):
        continue
    led_manager(L3,Off)

        
def rx_mode(): 
    led_manager(L2,On)
    #AQUI cridar les funcions necesaries per a executar el rx mode
    #radio = RF24(22, 0)

    #if not radio.begin():
    #    raise OSError("nRF24L01 hardware isn't responding")

    #radio_setup(12345, True)
    radioSetupRX()
    
    reception = rx()

    #encendre leds en funció del valor de "reception[0]"
    if reception[0]:
        print("OK")
        #encendre un led
    elif not reception[0]:
        print("NOT OK")
        #encendre un altre led

    write(reception[1])

    radio.power = False
    while (GPIO.input(SW6)==True):
        continue
    led_manager(L2,Off)

        
#estat de inici 
while True:
    sleep(2)
    if GPIO.input(SW1)==True:
        led_manager(L_vermell,On)
        active()
        led_manager(L_vermell,Off)

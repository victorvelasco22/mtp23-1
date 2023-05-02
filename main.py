import RPi.GPIO as GPIO #importem la llibreria correpsonent
from functions import *
from pyrf24 import RF24
from time import sleep

GPIO.setmode(GPIO.BCM) #establim com es fara referencia als pins de la RPi

#establim com es fara referencia als pins de la RPi
SW1=13 #active/stand by
SW2=19 #tx/rx
SW3=26 #fm/nm
SW4=21 #load usb
SW5=20 #unload usb
SW6=16 #go/stop
SW7=12

#establim els pins conectats als switches com a inputs
GPIO.setup(SW1, GPIO.IN)
GPIO.setup(SW2, GPIO.IN)
GPIO.setup(SW3, GPIO.IN)
GPIO.setup(SW4, GPIO.IN)
GPIO.setup(SW5, GPIO.IN)
GPIO.setup(SW6, GPIO.IN)
GPIO.setup(SW7, GPIO.IN)

#definicio dels diferents estats necesaris per a fer el main.
def active():
    while (SW1==True): #pasem a active mode
        sleep(0.5)
        
        
        if (SW4==True): #load usb
            read_usb()
        elif (SW5==True): #unload usb
            write_usb()
        elif (SW6==True & SW3==True): #network mode
            network_mode()
        elif (SW6==True & SW3==False & SW2==False): #rx
            rx_mode()
        elif (SW6==True & SW3==False & SW2==True): #tx
            tx_mode()
    
def read_usb():
    #AQUI cridar les funcions necesaries per a llegir del usb
    #Llegir del usb i copiar-ho al directori corresponent de la funció "open_txt()"
    while (SW4==True):
        continue

def write_usb():
    #AQUI cridar les funcions necesaries per a escriure al usb
    #Llegir-ho del directori on ho guarda la funció "write()" i copiar-ho al pen
    while (SW5==True):
        continue

def network_mode():
    #AQUI cridar les funcions necesaries per a executar el network mode
    while (SW6==True):
        continue

def tx_mode(): 
    #AQUI cridar les funcions necesaries per a executar el tx mode
    radio = RF24(22, 0)

    if not radio.begin():
        raise OSError("nRF24L01 hardware isn't responding")

    radio_setup(12345, False)

    payload = frament_the_text(compress(open_txt()))

    ok = tx(payload)

    #encendre leds en funció del valor de "ok"
    if ok:
        continue
        #encendre un led
    elif not ok:
        continue
        #encendre un altre led

    radio.power = False
    
    while (SW6==True):
        continue

def rx_mode(): 
    #AQUI cridar les funcions necesaries per a executar el rx mode
    radio = RF24(22, 0)

    if not radio.begin():
        raise OSError("nRF24L01 hardware isn't responding")

    radio_setup(12345, True)

    reception = rx()

    #encendre leds en funció del valor de "reception[0]"
    if reception[0]:
        continue
        #encendre un led
    elif not reception[0]:
        continue
        #encendre un altre led

    write(reception[1])

    radio.power = False
    while (SW6==True):
        continue

#estat de inici 
while True:
    sleep(2)
    if SW1==True:
        active()

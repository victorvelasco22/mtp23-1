import RPi.GPIO as GPIO #importem la llibreria correpsonent
from functions import *
from pyrf24 import RF24
import struct

GPIO.setmode(GPIO.BCM) #establim com es fara referencia als pins de la RPi

#establim com es fara referencia als pins de la RPi
SW1=13
SW2=19
SW3=26
SW4=21
SW5=20
SW6=16
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
    while (SW1==True):
        if (SW4==True):
            read_usb()
        elif (SW5==True):
            write_usb()
        elif (SW6==True & SW3==True):
            network_mode()
        elif (SW6==True & SW3==False & SW2==False):
            rx_mode()
        elif (SW6==True & SW3==False & SW2==True):
            tx_mode()
    
def read_usb():
    #AQUI cridar les funcions necesaries per a llegir del usb
    #Llegir del usb i copiar-ho al directori corresponent de la funció "open_txt()"
    while (SW4==True):
        continue

def write_usb():
    #AQUI cridar les funcions necesaries per a escriure al usb
    while (SW5==True):
        continue

def network_mode():
    #AQUI cridar les funcions necesaries per a executar el network mode
    while (SW6==True):
        continue

def tx_mode(): 
    #AQUI cridar les funcions necesaries per a executar el tx mode
    while (SW6==True):
        radio = RF24(22, 0)
        
        if not radio.begin():
            raise OSError("nRF24L01 hardware isn't responding")
        
        radio_setup(12345, False)
        
        payload = frament_the_text(compress(open_txt()))
        
        ok = tx(payload)
        #encendre leds en funció del valor de "ok"
        continue

def rx_mode(): 
    #AQUI cridar les funcions necesaries per a executar el rx mode
    while (SW6==True):
        continue

#estat de inici 
while True:
    if SW1==True:
        active()

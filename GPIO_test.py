import RPi.GPIO as GPIO #importem la llibreria correpsonent
import time

GPIO.setmode(GPIO.BCM) #establim com es fara referencia als pins de la RPi

L_vermell=2
L2=27
L3=22
L4=9
L5=11

SW1=13
SW2=19
SW3=26
SW4=21
SW5=20
SW6=16
SW7=12

On=True
Off=False

GPIO.setup(L_vermell, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
GPIO.setup(L5, GPIO.OUT)

GPIO.setup(SW1, GPIO.IN)
GPIO.setup(SW2, GPIO.IN)
GPIO.setup(SW3, GPIO.IN)
GPIO.setup(SW4, GPIO.IN)
GPIO.setup(SW5, GPIO.IN)
GPIO.setup(SW6, GPIO.IN)
GPIO.setup(SW7, GPIO.IN)

GPIO.output(L_vermell, GPIO.LOW)
GPIO.output(L2, GPIO.LOW)
GPIO.output(L3, GPIO.LOW)
GPIO.output(L4, GPIO.LOW)
GPIO.output(L5, GPIO.LOW)

def led_manager(color, estat):
  if(estat):
    GPIO.output(color, GPIO.HIGH)

  else:
    GPIO.output(color, GPIO.LOW)



#definicio dels diferents estats necesaris per a fer el main.
def active():
    while (GPIO.input(SW1)==True):
        led_manager(L_vermell,On)
        if (GPIO.input(SW7)==True):
            led_manager(L1,Off)
            read_usb()
        elif (GPIO.input(SW5)==True):
            led_manager(L1,Off)
            write_usb()
        elif (GPIO.input(SW6)==True & GPIO.input(SW3)==True):
            led_manager(L1,Off)
            network_mode()
        elif (GPIO.input(SW6)==True & GPIO.input(SW3)==False & GPIO.input(SW2)==False):
            led_manager(L1,Off)
            rx_mode()
        elif (GPIO.input(SW6)==True & GPIO.input(SW3)==False & GPIO.input(SW2)==True):
            led_manager(L_vermell,Off)
            tx_mode()
    
def read_usb():
    #AQUI cridar les funcions necesaries per a llegir del usb
    led_manager(L5,On)
    while (GPIO.input(SW7)==True):
        continue
    led_manager(L5,Off)


def write_usb():
    #AQUI cridar les funcions necesaries per a escriure al usb
    led_manager(L4,On)
    while (GPIO.input(SW5)==True):
        continue
    led_manager(L4,Off)


def network_mode():
    #AQUI cridar les funcions necesaries per a executar el network mode
    led_manager(L3,On)
    led_manager(L2,On)
    while (GPIO.input(SW6)==True):
        continue
    led_manager(L3,Off)
    led_manager(L2,Off)

def tx_mode(): 
    #AQUI cridar les funcions necesaries per a executar el network mode
    led_manager(L3,On)
    while (GPIO.input(SW6)==True):
        continue
    led_manager(L3,Off)


def rx_mode(): 
    #AQUI cridar les funcions necesaries per a executar el network mode
    led_manager(L2,On)
    while (GPIO.input(SW6)==True):
        continue
    led_manager(L2,Off)


#estat de inici 
while True:
    print("1")
    print(GPIO.input(SW1))
    print("2")
    print(GPIO.input(SW2))
    print("3")
    print(GPIO.input(SW3))
    print("4")
    print(GPIO.input(SW4))
    print("5")
    print(GPIO.input(SW5))
    print("6")
    print(GPIO.input(SW6))
    print("7")
    print(GPIO.input(SW7))
    time.sleep(2)
    if GPIO.input(SW1)==True:
        active()


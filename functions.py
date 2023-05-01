import os
from glob import glob
from subprocess import check_output, CalledProcessError
import bz2

EOF = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF' 
EOF1 = (0, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
EOF2 = (1, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')

#radio setup
#mode = False for TX or True for RX
def radio_setup(addr, mode):
  radio.setPALevel(2,1)
  radio.openReadingPipe(0,addr)
  radio.channel = 90
  radio.listen = mode
  radio.print_pretty_details()


#CHANGE FILE PATH/NAME
#read the utf-16-le file
def open_txt():
  with open("/home/rpi/mtp23/test_file_16_utf_le_1MB.txt", "rb") as f:
        text = f.read()
  return text

#encoding of the text to utf-16-le for compression, NOT USED NOT
def encodes(text):
  return text.encode(encoding='utf-16-le', errors='strict')

#decode the text back to utf-16, NOT USED NOT
def decodes(text):
  return text.decode(encoding='utf-16-le', errors='strict')

#fragment text in a list elements of 31 bytes (the first one is the sequence number)
def frament_the_text(text):
  payload = list()
  for i in range(0,len(text), 31):
    payload.append(text[i:i+31])
  return payload

def compress(text_to_tx):
  # preset = 9 -> max compression, but slowest
  return bz2.compress(text_to_tx, compresslevel=9)

def decompress(compressed_txt):
    return bz2.decompress(compressed_txt)

#TO DO: read pins

#funcions per a detectar el path fins el directori del pendrive
def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_points(devices=None):
    devices = devices or get_usb_devices()  # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    output = [tmp.decode('UTF-8') for tmp in output]

    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [(info.split()[0], info.split()[2]) for info in usb_info] #el primer valor es el Filesystem i el segon es on esta ubicat el directori del pendrive.


def read_from_pen():                #obtenció del path fins al pendrive i coversió de fitxer .txt a string, el output de la funció es "data" que es el .txt convertit a string.
    dir=get_mount_points()[0][1]    #obtenció del directori de usb (dir).
    os.chdir(dir)                   #establim el directori del usb(dir) com a directori de treball.
    for file in glob("*.txt"):      #es localitza el fitxer .txt.
        print(file)
    with open(file, 'r') as file:   #es converteix el fitxer .txt a string.
        data = file.read()
    return data


def write_on_pen(data):                         #obtenció del path fins al pendrive i escriptura en forma de .txt de la variable data que es una string en el pendrive.
    dir=get_mount_points()[0][1]                #obtenció del directori de usb (dir).
    os.chdir(dir)                               #establim el directori del usb(dir) com a directori de treball.
    with open("Output.txt", "w") as text_file:  #es converteix string(data) a fitxer .txt(Output.txt).
        text_file.write(data)


        #controlador pels leds
import RPi.GPIO as GPIO  #importem la llibreria correpsonent

GPIO.setmode(GPIO.BCM) #establim com es fara referencia als pins de la RPi

#Definim constants per a referirnos als Leds de una manera més senzilla
L1=17
L2=27
L3=22
L4=9
L5=11

#establim els pins conectats als leds com a outputs
#GPIO.setup(L1, GPIO.OUT)
#GPIO.setup(L2, GPIO.OUT)
#GPIO.setup(L3, GPIO.OUT)
#GPIO.setup(L4, GPIO.OUT)
#GPIO.setup(L5, GPIO.OUT)

#def led_manager(led, estat): #funció per a operar els leds, es donen com a inputs el led i l'estat del led (On/Off) per a fer el funcionament d'aquests
#  if(estat):
#    GPIO.output(led, GPIO.HIGH) #obrir el led

#  else:
#    GPIO.output(led, GPIO.LOW) #tencar el led


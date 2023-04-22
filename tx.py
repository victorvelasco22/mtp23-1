import struct
import time
from pyrf24 import RF24
import bz2

# FUNCTIONS

#read the utf-16-le file
def open_txt():
  with open("/home/rpi/helloworld.txt", "rb") as f:
        text = f.read().decode("utf-16-le", errors="strict")
  return text

#encoding of the text to utf-16-le for compression
def encodes(text):
  return text.encode(encoding='utf-16-le', errors='strict')

#decode the text back to utf-16
def decodes(text):
  return text.decode(encoding='utf-16-le', errors='strict')

#fragment text in blocks of 32 bytes
def frament_the_text(text):
  payload = list()
  for i in range(0,len(text), 32):
    payload.append(text[i:i+32])
  return payload

# MAIN

radio = RF24(22, 0)

#TO DO: migrate to functions.py
EOF = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF' 

# initialize the nRF24L01 on the spi bus
if not radio.begin():
  raise OSError("nRF24L01 hardware isn't responding")

#RADIO SETUP
address=12345
radio.setPALevel(2,1)
radio.openWritingPipe(address)
radio.channel = 90
radio.setPayloadSize(struct.calcsize("<32s"))
radio.print_pretty_details()

packets_sent = 0

#READ THE FILE (Joan)
#TO DO: always listening and detect the file automatically
original_text = open_txt()
text_to_tx = encodes(original_text)

#COMPRESSION (Josep)
# preset = 9 -> max compression, but slowest
text_compressed = lzma.compress(text_to_tx, preset=9)

#FRAGMENT THE COMPRESSED TEXT IN BLOCKS OF 32 BYTES
payload = frament_the_text(text_compressed)

#PUT DEVICE IN TX MODE
radio.listen = False
ok = False

#START THE TRANSMISSION
try:
  for i in range(len(payload)):
    message = struct.pack("<32s",payload[i])
    ok = radio.write(message)
    packets_sent += 1
    #print(f"Sending {packets_sent}...", ("ok" if ok else "failed"))
    print(message)
  message = struct.pack("<32s",EOF)
  ok = radio.write(message)
  
  if ok:
    print("Transmission complete")
  else:
    print("Transmission failed")
  fichero.close()
  radio.power = False
except KeyboardInterrupt:
  print("powering down radio and exiting.")
  radio.power = False

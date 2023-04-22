import struct
import time
from pyrf24 import RF24

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
fichero = open("/home/rpi/helloworld.txt", "rb")
text = fichero.read()

#COMPRESSION (Josep)

#FRAGMENT THE COMPRESSED TEXT IN BLOCKS OF 32 BYTES
payload = list()
for i in range(0,len(text), 32):
  payload.append(text[i:i+32])

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

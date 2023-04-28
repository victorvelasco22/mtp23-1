import struct
import time
from pyrf24 import RF24
import bz2
from functions import  *
  
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
radio.setRetries(10,15)
radio.openWritingPipe(address)
radio.channel = 90
radio.setPayloadSize(struct.calcsize("<32s"))
radio.print_pretty_details()

packets_sent = 0

#READ THE FILE
#TO DO: always listening and detect the file automatically (Joan)
bytes_to_tx = open_txt()

#COMPRESSION (Josep)
bytes_compressed = compress(bytes_to_tx)

#FRAGMENT THE COMPRESSED TEXT IN BLOCKS OF 32 BYTES
payload = frament_the_text(bytes_compressed)
print("Num packets: " + str(len(payload)))

#PUT DEVICE IN TX MODE
radio.listen = False
ok = False

#START THE TRANSMISSION
try:
  for i in range(len(payload)):
    message = struct.pack("<32s",payload[i])
    ok = False
    while not ok:
      ok = radio.write(message)
      packets_sent += 1
      print(f"Sending {packets_sent}...", ("ok" if ok else "failed"))
    #print(message)
  message = struct.pack("<32s",EOF)
  ok = radio.write(message)
  
  if ok:
    print("Transmission complete")
  else:
    print("Transmission failed")
  #fichero.close()
  radio.power = False
except KeyboardInterrupt:
  print("powering down radio and exiting.")
  radio.power = False

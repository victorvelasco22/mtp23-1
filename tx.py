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

total_packets_sent = 0
packets_sent_ok = 0
packets_sent_failed = 0
seq_num = 0x00

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
    message = struct.pack("<B32s",seq_num,payload[i])
    ok = False
    #Infinite retries
    while not ok:
      ok = radio.write(message)
      total_packets_sent += 1
      print(f"Sending {total_packets_sent}...", ("ok" if ok else "failed"))
      if not ok:
        packets_sent_failed += 1
    packets_sent_ok += 1
    #Changing sequence number
    if seq_num == 0x00:
      seq_num = 0x01
    else if seq_num == 0x01:
      seq_num = 0x00
    #print(message)
  #Sending EOF
  message = struct.pack("<B32s",seq_num,EOF)
  ok = radio.write(message)
  while not ok:
      ok = radio.write(message)
      total_packets_sent += 1
      print(f"Sending {total_packets_sent}...", ("ok" if ok else "failed"))
  if ok:
    print("Transmission complete")
  else:
    print("Transmission failed")
  #fichero.close()
  radio.power = False
except KeyboardInterrupt:
  print("powering down radio and exiting.")
  radio.power = False

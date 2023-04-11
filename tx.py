import struct
import time
from pyrf24 import RF24

radio = RF24(22, 0)

EOF = '/0xFF'

# initialize the nRF24L01 on the spi bus
if not radio.begin():
  raise OSError("nRF24L01 hardware isn't responding")

radio.channel = 90
radio.print_pretty_details()

packets_sent = 0

fichero = open("/home/hector/helloworld.txt", "r")
text = fichero.read()
text_bytes = bytearray(text,'utf-8')

#number of fragments with max payload (32 bytes)
num_fragments = len(text_bytes) // 32

#we create a payload list of 32 bytes
payload = []
j = 0
for i in range(num_fragments):
  payload.append([])
  payload[i].append(text_bytes[j:j+31])
  j += 32
#we fill the list with the remaining bytes
remaining = len(text_bytes)%32
payload.append([])
payload[num_fragments].append(text_bytes[j:j+remaining]) 

#put device in TX mode
radio.listen = false

try:
  for i in range(len(payload)-1):
    message = struct.pack("<32s",payload[i])
    ok = radio.write(message)
    packets_sent += 1
    print(f"Sending {packets_sent}...", ("ok" if ok else "failed"))
  
  message = struct.pack("<{remaining}s",payload[len(payload)-1])
  ok = radio.write(message)
  packets_sent += 1
  print(f"Sending {packets_sent}...", ("ok" if ok else "failed"))
    
  message = struct.pack("<B",EOF)
  ok = radio.write(message)
  
  if ok:
    print("Transmission complete")
  else:
    print("Transmission failed")
  
except KeyboardInterrupt:
  print("powering down radio and exiting.")
  radio.power = False

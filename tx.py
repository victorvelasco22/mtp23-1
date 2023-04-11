import struct
import time
from pyrf24 import RF24

radio = RF24(22, 0)

EOF = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF' 

# initialize the nRF24L01 on the spi bus
if not radio.begin():
  raise OSError("nRF24L01 hardware isn't responding")

#radio setup
address=b'\xAB\xAB\xAB\xAB\xAB'
radio.openWritingPipe(address)
radio.channel = 90
radio.setPayloadSize(struct.calcsize("<32s"))
radio.print_pretty_details()

packets_sent = 0

#read the file
fichero = open("/home/hector/helloworld.txt", "rb")
text = fichero.read()
#text_bytes = bytes(text,'utf-8')
#text_bytes = text

#fragment text in blocks of 32 bytes
payload = list()
for i in range(0,len(text), 32):
  payload.append(text[i:i+32])

#number of fragments with max payload (32 bytes)
#num_fragments = len(text_bytes) // 32

#we create a payload list of 32 bytes
#payload = []
#j = 0
#for i in range(num_fragments):
#  payload.append([])
#  payload[i].append(text_bytes[j:j+31])
#  j += 32
#we fill the list with the remaining bytes
#remaining = len(text_bytes)%32
#payload.append([])
#payload[num_fragments].append(text_bytes[j:j+remaining]) 

#put device in TX mode
radio.listen = False
ok = False

try:
  for i in range(len(payload)):
    message = struct.pack("<32s",payload[i])
    #start = time.monotonic_ns()
    ok = radio.write(message)
    #end = time.monotonic_ns()
    packets_sent += 1
    print(f"Sending {packets_sent}...", ("ok" if ok else "failed"))
    print(message)
  message = struct.pack("<32s",EOF)
  ok = radio.write(message)
  #message = struct.pack("<{remaining}s",payload[len(payload)-1])
  #ok = radio.write(message)
  #packets_sent += 1
  #print(f"Sending {packets_sent}...", ("ok" if ok else "failed"))
    
  #message = struct.pack("<B",EOF)
  #ok = radio.write(message)
  if ok:
    print("Transmission complete")
  else:
    print("Transmission failed")
  radio.power = False
except KeyboardInterrupt:
  print("powering down radio and exiting.")
  radio.power = False

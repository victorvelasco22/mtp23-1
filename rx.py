import struct
from pyrf24 import RF24

EOF = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF' 

radio = RF24(22, 0)

#EOF = '/0xFF'

if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

radio.channel = 90
radio.print_pretty_details()
radio.listen = True

eof = False
payload = []
received_packets = 0

try:
    while not eof:
        if radio.available():
            buffer = radio.read()
            fragment = struct.unpack("<32s",buffer)
            if fragment == EOF:
                eof = True
            else:
                payload.append(fragment)
                received_packets += 1
    print("Transmission ok")
    print(payload) 
    text = str(payload,'utf-8')
    print(text)
    radio.power = False
    
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False

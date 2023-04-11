import struct
from pyrf24 import RF24

EOF = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF' 

radio = RF24(22, 0)

if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

#radio setup
address=12345
radio.openReadingPipe(0,address)
radio.channel = 90
radio.listen = True
radio.print_pretty_details()

fichero = open("/home/rpi/output.txt", "wb")

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
                print(fragment)
                payload.append(fragment)
                fichero.write(fragment)
                received_packets += 1
    print(f"Transmission ok, total received packets: {received_packets}")
    print(payload) 
    text = str(payload,'utf-8')
    print(text)
    radio.power = False
    
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False

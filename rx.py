import struct
from pyrf24 import RF24

radio = RF24(22, 0)

EOF = '/0xFF'

if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

radio.channel = 90
radio.listen = true

eof = False
payload = bytearray()

try:
    while not eof:
        if radio.available():
            packet = radio.read()
            if struct.unpack("<B",packet) == EOF:
                eof = True
            else:
                payload.append(struct.unpack("<32s",packet))
    
    print("Transmission ok")
    text = str(payload,'utf-8')
    print(text)
    radio.power = False
    
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False

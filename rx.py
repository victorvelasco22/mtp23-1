import struct
from pyrf24 import RF24
import bz2

# FUNCTIONS
#decode the text back to utf-16
def decodes(text):
  return text.decode(encoding='utf-16-le', errors='strict')

# MAIN
EOF = (b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF',)

radio = RF24(22, 0)

if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

#radio setup
#radio.setDataRate(2)-> This is to change the data rate to 250Kbps. Default is 1Mbps (1)
radio.setPALevel(2,1)
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
                #for i in range(len(fragment)):
                #    fichero.write(fragment[i])
                payload.append(fragment)
                received_packets += 1
    compressed_txt = ".".join(payload)
    decompressed_txt = decodes(zlib.decompress(compressed_txt))
    fichero.write(decompressed_txt.encode("utf-16-le", errors="strict")))
    print(f"Transmission ok, total received packets: {received_packets}")
    #print(payload)
    fichero.close()
    radio.power = False
    
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False

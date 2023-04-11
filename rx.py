import struct
from pyrf24 import RF24

radio = RF24(22, 0)

if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

radio.channel = 90
radio.listen = true

eof = false

try:
    while not eof:
        while network.available():
            header, payload = network.read()
            print("payload length ", len(payload))
            millis, packet_count = struct.unpack("<LL", payload[:EXPECTED_SIZE])
            print(
                f"Received payload {packet_count} at (origin's timestamp) {millis}.",
                f"Header details {header.to_string()}",
            )
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False

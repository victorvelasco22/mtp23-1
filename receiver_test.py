import argparse
from datetime import datetime
import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *


#
# A simple NRF24L receiver that connects to a PIGPIO instance on a hostname and port, default "localhost" and 8888, and
# starts receiving data on the address specified.  Use the companion program "simple-sender.py" to send data to it from
# a different Raspberry Pi.
#
if __name__ == "__main__":

    print("Receiver test")
    
    # Parse command line argument.
    parser = argparse.ArgumentParser(prog="simple-receiver.py", description="Simple NRF24 Receiver Example.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
    parser.add_argument('address', type=str, nargs='?', default='1SNSR', help="Address to listen to (3 to 5 ASCII characters)")

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    address = args.address

    # Verify that address is between 3 and 5 characters.
    if not (2 < len(address) < 6):
        print(f'Invalid address {address}. Addresses must be between 3 and 5 ASCII characters.')
        sys.exit(1)
    
    # Connect to pigpiod
    print(f'Connecting to GPIO daemon on {hostname}:{port} ...')
    pi = pigpio.pi(hostname, port)
    if not pi.connected:
        print("Not connected to Raspberry Pi ... goodbye.")
        sys.exit()

    # Aqui podemos especificar el data rate
    # Create NRF24 object.
    # PLEASE NOTE: PA level is set to MIN, because test sender/receivers are often close to each other, and then MIN works better.
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.MIN)
    nrf.set_address_bytes(len(address))

    # Listen on the address specified as parameter
    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)
    
    # Display the content of NRF24L01 device registers.
    nrf.show_registers()
    
    text="Hello world"
    print(f"Original: {text}")
    text_bytes = bytes(text,'utf-8')
    print(f"Bytes: {text_bytes}")
    length = len(text_bytes)
    print(f"Number of bytes: {sys.getsizeof(text_bytes)}")
    payload = struct.pack("<B11s", 0x01, text_bytes)
    print(f"Payload packed: {payload}")
    print("----TRANSMISSION----")
    payload_unpack = struct.unpack("<B11s", payload)
    print(f"Unpacked payload: {payload_unpack}")
    sin_flags=payload_unpack[1]
    print(f"Payload sin flags: {sin_flags}")
    text_decoded = bytes.decode(sin_flags,'utf-8')
    print(f"Text decoded: {text_decoded}")
    
    # Enter a loop receiving data on the address specified.
    try:
        print(f'Receive from {address}')
        count = 0
        
        # Ha de estar todo el rato escuchando
        while True:

            # As long as data is ready for processing, process it.
            while nrf.data_ready():
                # Count message and record time of reception.            
                count += 1
                now = datetime.now()
                
                # Read pipe and payload for message.
                pipe = nrf.data_pipe()
                payload = nrf.get_payload()        

                # Opcional
                # Lee los bytes (i) del payload recibido y los concatena con : escribiendolos en hexadecimal con longitud mínima 2
                hex = ':'.join(f'{i:02x}' for i in payload)

                # Show message received as hex.
                print(f"{now:%Y-%m-%d %H:%M:%S.%f}: pipe: {pipe}, len: {len(payload)}, bytes: {hex}, count: {count}")

                #Si la trama es de longitud maxima (o lleva el EOF) y el primer byte es 0x01, la decodificamos
                #Falta cambiar la condición. De momento pongo solo lo del primer byte
                #Decodificar bytes con utf-8
                #Gestionar las flags de la trama
                if payload[0] == 0x01:
                    text_bytes = struct.unpack("<B11s", payload)
                    text = bytes.decode(text_bytes, 'utf-8')
                    print(f'Received data: {text}')
                
            # Sleep 100 ms.
            time.sleep(0.1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()

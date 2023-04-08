import argparse
from datetime import datetime
from random import normalvariate
import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *

#
# A simple NRF24L sender that connects to a PIGPIO instance on a hostname and port, default "localhost" and 8888, and
# starts sending data on the address specified.  Use the companion program "simple-receiver.py" to receive the data
# from it on a different Raspberry Pi.
#
if __name__ == "__main__":    
    print("Sender test")
    
    # Parse command line argument.
    parser = argparse.ArgumentParser(prog="simple-sender.py", description="Simple NRF24 Sender Example.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
    parser.add_argument('address', type=str, nargs='?', default='1SNSR', help="Address to send to (3 to 5 ASCII characters).")
    
    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    address = args.address

    if not (2 < len(address) < 6):
        print(f'Invalid address {address}. Addresses must be 3 to 5 ASCII characters.')
        sys.exit(1)

    # Connect to pigpiod
    print(f'Connecting to GPIO daemon on {hostname}:{port} ...')
    pi = pigpio.pi(hostname, port)
    if not pi.connected:
        print("Not connected to Raspberry Pi ... goodbye.")
        sys.exit()

    # Aqui podemos especificar el data rate.
    # Create NRF24 object.
    # PLEASE NOTE: PA level is set to MIN, because test sender/receivers are often close to each other, and then MIN works better.
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.LOW)
    nrf.set_address_bytes(len(address))
    nrf.open_writing_pipe(address)
    
    # Display the content of NRF24L01 device registers.
    nrf.show_registers()

    try:
        print(f'Send to {address}')
        count = 0
        fin = 0
        while fin < 1:    
            
            #Aqui seria leer el fichero de texto.
            #Suponemos que guardamos el contenido de fichero en la variable "text"
            # text="Hello world"
            # print(f'Contenido del fichero: {text}')
            
            text = open("/home/rpi/helloworld.txt", "r")
            print(f'Contenido del fichero: {text}')
            
            #Falta parsearlo para enviar tramas de una longitud máxima. No podemos enviar texto de longitud infinita.
            #Falta incluir el EOF

            #Convertimos el texto en bytes (codificamos con UTF-8)
            text_bytes = bytes(text,'utf-8')
           
            #Empaquetamos en un buffer (payload) poniendo el primer byte a 00000001 (0x01) para que lo reconozca el receptor
            #Esto se tendrá que cambiar con los numeros de secuencia, ACK, y demás flags que tenga la trama
            #B para el primer byte
            #11s pq 'Hello world' tiene 11 caracteres. Hay que adaptarlo al tamaño de la trama
            # payload = struct.pack("<B11s", 0x01, text_bytes)

            payload = text_bytes
            
            # Send the payload to the address specified above.
            nrf.reset_packages_lost()
            nrf.send(payload)
            try:
                nrf.wait_until_sent()
            except TimeoutError:
                print('Timeout waiting for transmission to complete.')
                # Wait 10 seconds before sending the next reading.
                time.sleep(10)
                continue
            print("sent OK!")
            
            #Seguir leyendo datos en bloques de lmax hasta el EOF.
            #Cuando lea el EOF, que ponga fin = 1 para cerrar la TX.
            fin = 1
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()

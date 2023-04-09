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
        
        # Ruta fichero pen drive
        fichero = open("/home/rpi/helloworld.txt", "r")
        text = fichero.read()
        print(f'Contenido del fichero: {text}')
        print(f'Numero de bytes: {sys.getsizeof(text)}')
      
        #Convertimos el texto en bytes (codificamos con UTF-8)
        text_bytes = bytes(text,'utf-8')
        print(f'Contenido del fichero pasado a bytes: {text_bytes}')
        print(f'Numero de bytes: {sys.getsizeof(text_bytes)}')
        
        # Falta parsearlo para enviar tramas de una longitud máxima. No podemos enviar texto de longitud infinita.
        # Falta incluir el EOF
        # Lo hace automáticamente???
                   
        #Empaquetamos en un buffer (payload) poniendo el primer byte a 00000001 (0x01) para que lo reconozca el receptor
        #Esto se tendrá que cambiar con los numeros de secuencia, ACK, y demás flags que tenga la trama ---> Lo hace automaticamente??
        #B para el primer byte
        #11s pq 'Hello world' tiene 11 caracteres. Hay que adaptarlo al tamaño de la trama
        # payload = struct.pack("<B11s", 0x01, text_bytes)

            
        # Send the payload to the address specified above.
        nrf.reset_packages_lost()
        nrf.send(text)
        try:
            nrf.wait_until_sent()
        except TimeoutError:
            print('Timeout waiting for transmission to complete.')
            # Wait 10 seconds before sending the next reading.
            time.sleep(10)
        if not timeout:
                if nrf.get_packages_lost() == 0:    
                    # Check if an acknowledgement package is available.
                    if nrf.data_ready():
                        # Get payload.
                        payload = nrf.get_payload()
        
                        if len(payload) == 4:
                            # If the payload is 4 bytes, we expect it to be an acknowledgement payload.
                            (next_id, ) = struct.unpack('<I', payload)

                        else:
                            # Not 4 bytes long then we consider it an invalid payload.
                            print("Invalid acknowledgement payload received.")
                            next_id = -1
                    else:
                        print("No acknowledgement package received.")
                        next_id = -1
    
                else:
                    # The package sent was lost.
                    print("Package lost. No acknowledgement.")
                    next_id = -1
            else:
                print("Timeout. No acknowledgement.")
                next_id = -1


            if timeout:
                print(f'Error: timeout while waiting for acknowledgement package. next_id={next_id}')
            else:  
                if nrf.get_packages_lost() == 0:
                    # The package we sent was successfully received by the server.
                    print(f"Success: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}, next_id={next_id}")
                else:
                    print(f"Error: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}, next_id={next_id}")
            
            # Wait 10 seconds before sending the next reading.
            time.sleep(10)
            
        print("sent OK!")
        fichero.close()    
        
        #Seguir leyendo datos en bloques de lmax hasta el EOF.
        #Cuando lea el EOF, que ponga fin = 1 para cerrar la TX.
        #Lo hace solo??
        
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()

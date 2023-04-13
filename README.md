# mtp23

## Raspberry configuration:
``$sudo apt install python3-rpi.gpio``\
``$python -m pip install pyrf24``\
``$sudo apt install git``\
``$git clone https://github.com/victorvelasco22/mtp23/``\
``$touch output.txt``\
``$nano helloworld.txt`` -> and write the text to be sent

## Execution
``$python mtp23/rx.py`` -> Receiver \
``$python mtp23/tx.py`` -> Transmitter

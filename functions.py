import os
from glob import glob
from subprocess import check_output, CalledProcessError

#

#TO DO: read pins

#TO DO: compression

#TO DO: decompression

#TO DO: agrupar-ho en funcions

#funcions per a detectar el path fins el directori del pendrive
def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_points(devices=None):
    devices = devices or get_usb_devices()  # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    output = [tmp.decode('UTF-8') for tmp in output]

    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [(info.split()[0], info.split()[2]) for info in usb_info] #el primer valor es el Filesystem i el segon es on esta ubicat el directori del pendrive.


def read_from_pen():                #obtenció del path fins al pendrive i coversió de fitxer .txt a string, el output de la funció es "data" que es el .txt convertit a string.
    dir=get_mount_points()[0][1]    #obtenció del directori de usb (dir).
    os.chdir(dir)                   #establim el directori del usb(dir) com a directori de treball.
    for file in glob("*.txt"):      #es localitza el fitxer .txt.
        print(file)
    with open(file, 'r') as file:   #es converteix el fitxer .txt a string.
        data = file.read()
    return data


def write_on_pen(data):                         #obtenció del path fins al pendrive i escriptura en forma de .txt de la variable data que es una string en el pendrive.
    dir=get_mount_points()[0][1]                #obtenció del directori de usb (dir).
    os.chdir(dir)                               #establim el directori del usb(dir) com a directori de treball.
    with open("Output.txt", "w") as text_file:  #es converteix string(data) a fitxer .txt(Output.txt).
        text_file.write(data)

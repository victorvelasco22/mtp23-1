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
    return [(info.split()[0], info.split()[2]) for info in usb_info] #el primer valor es el Filesystem i el segon es on esta ubicat el directori del pendrive

dir=get_mount_points()[0][1]


#establim el directori del usb com a directori de treball
os.chdir(dir)

#es localitza el fitxer .txt
for file in glob("*.txt"):
    print(file)

#es converteix el fitxer .txt a string
with open(file, 'r') as file:
    data = file.read()

#es converteix string a fitxer .txt
with open("Output.txt", "w") as text_file:
    text_file.write(data)

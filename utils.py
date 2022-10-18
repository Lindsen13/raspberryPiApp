import os
import glob
 
def read_temperature() -> float:
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
 
    file_path = f"{glob.glob('/sys/bus/w1/devices/' + '28*')[0]}/w1_slave"

    with open(file_path, 'r') as f:
        data = f.read()
    return int(data.split('t=')[-1].strip()) / 1000

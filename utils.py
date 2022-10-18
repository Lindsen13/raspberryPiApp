from sqlalchemy import create_engine, engine
import glob
import os


def read_temperature() -> float:
    if os.environ.get('local') == 'true':
        # Return -1 when we're developing locally.
        temperature = float(-1)
    else:
        # Return temperature fetched from sensor.
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        file_path = f"{glob.glob('/sys/bus/w1/devices/' + '28*')[0]}/w1_slave"
        with open(file_path, 'r') as f:
            data = f.read()
        temperature = int(data.split('t=')[-1].strip()) / 1000
    return temperature

def construct_engine() -> engine.Engine:
    return create_engine(f"mysql+pymysql://{os.environ.get('mysql_user')}:{os.environ.get('mysql_password')}@{os.environ.get('mysql_host')}:{os.environ.get('mysql_port')}/{os.environ.get('mysql_database')}?charset=utf8mb4")
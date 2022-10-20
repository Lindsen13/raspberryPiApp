from sqlalchemy import create_engine, engine
from bs4 import BeautifulSoup
import requests
import datetime
import pytz
import json
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

def read_electricity_price() -> float:
    url = 'https://andelenergi.dk/kundeservice/aftaler-og-priser/timepris/'

    output = requests.get(url)

    soup = BeautifulSoup(output.text, 'html.parser')
    soup.find(id='chart-component').get('data-chart')

    data = json.loads(soup.find(id='chart-component').get('data-chart'))
    data['east']['values'][-(24-datetime.datetime.now().hour)]
    hours_offset = -(24-datetime.datetime.now(pytz.timezone('Europe/Copenhagen')).hour)
    hourly_price = data.get('east',{}).get('values',[])[hours_offset]
    hourly_price = int(hourly_price.replace('.',''))/100
    return hourly_price





def construct_engine() -> engine.Engine:
    return create_engine(f"mysql+pymysql://{os.environ.get('mysql_user')}:{os.environ.get('mysql_password')}@{os.environ.get('mysql_host')}:{os.environ.get('mysql_port')}/{os.environ.get('mysql_database')}?charset=utf8mb4")
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

def read_internal_temperature() -> float:
    if os.environ.get('local') == 'true':
        # Return -1 when we're developing locally.
        return float(-1)
    else:
        # Return temperature fetched from sensor.
        internal_temp =  os.popen('vcgencmd measure_temp').read()
        internal_temp = internal_temp.split("'")[0].split('=')[-1]
        return int(internal_temp.replace('.',''))/10

def read_electricity_price() -> float:
    url = 'https://andelenergi.dk/kundeservice/aftaler-og-priser/timepris/'

    output = requests.get(url)

    soup = BeautifulSoup(output.text, 'html.parser')
    data = json.loads(soup.find(id='chart-component').get('data-chart'))
    
    hours_offset = -(24-datetime.datetime.now(pytz.timezone('Europe/Copenhagen')).hour)
    hourly_price = data.get('east',{}).get('values',[])[hours_offset]
    hourly_price = int(hourly_price.replace('.',''))/100
    return hourly_price

def read_future_electicity_price() -> list[dict[str,datetime.datetime|float]]:
    url = 'https://andelenergi.dk/kundeservice/aftaler-og-priser/timepris/'

    output = requests.get(url)

    soup = BeautifulSoup(output.text, 'html.parser')
    data = json.loads(soup.find(id='chart-component').get('data-chart'))

    data = data['east']['values'][-24:]
    output = []
    for hour, temp in enumerate(data):
        output.append(
            {
                'date':datetime.datetime(
                    year = datetime.datetime.now(pytz.timezone('Europe/Copenhagen')).year, 
                    month = datetime.datetime.now(pytz.timezone('Europe/Copenhagen')).month, 
                    day = datetime.datetime.now(pytz.timezone('Europe/Copenhagen')).day, 
                    hour = hour, 
                    minute = 0, 
                    second = 0,
                    tzinfo=pytz.timezone('Europe/Copenhagen')
                ),
                'electricity_price':int(temp.replace('.',''))/100
            }
        )
        
    return output

def construct_engine() -> engine.Engine:
    user = os.environ.get('mysql_user')
    pw = os.environ.get('mysql_password')
    host = os.environ.get('mysql_host')
    port = os.environ.get('mysql_port')
    db = os.environ.get('mysql_database')
    return create_engine(f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}?charset=utf8mb4")
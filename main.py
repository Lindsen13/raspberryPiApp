import datetime
from flask import Flask
from sqlalchemy.orm import Session
from utils import read_temperature, construct_engine, read_electricity_price
from db import Iot_data

app = Flask(__name__)

engine = construct_engine()

@app.route('/', methods=["GET"])
def index() -> str:
    return f"Hello world!"

@app.route('/temperature')
def temperature() -> dict[str,float]:
    temperature = read_temperature()
    with Session(engine) as session:
        temperature_value = Iot_data(
            name = 'Temperature',
            value = temperature
        )

        session.add(temperature_value)
        session.commit()
    print('Stored temperature!')
    return {"temperature":temperature}

@app.route('/electricity_price')
def electricity_price() -> dict[str, float]:
    el_price = read_electricity_price()
    with Session(engine) as session:
        electricity_price_value = Iot_data(
            name = 'Electricity Price',
            value = el_price
        )

        session.add(electricity_price_value)
        session.commit()
    print('Stored electricty price!')
    return {"electricy price":el_price, "datatime":str(datetime.datetime.now())}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
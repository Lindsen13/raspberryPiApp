import datetime
from flask import Flask
from sqlalchemy.orm import Session
from utils import read_temperature
from utils import construct_engine
from utils import read_electricity_price
from utils import read_internal_temperature
from utils import read_future_electicity_price
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

@app.route('/internal_temperature')
def internal_temperature() -> dict[str,float]:
    temperature = read_internal_temperature()
    with Session(engine) as session:
        temperature_value = Iot_data(
            name = 'Temperature Raspberry Pi',
            value = temperature
        )

        session.add(temperature_value)
        session.commit()
    print('Stored Raspberry Pi temperature!')
    return {"Raspberry Pi temperature":temperature}

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
    return {"electricy price":el_price}

@app.route('/future_electricity_price')
def future_electricity_price() -> dict[str, float]:
    el_price = read_electricity_price()
    with Session(engine) as session:
        electricity_price_value = Iot_data(
            name = 'Electricity Price',
            value = el_price
        )

        session.add(electricity_price_value)
        session.commit()
    print('Stored electricty price!')
    return {"electricy price":el_price}

@app.route('/future_electicity_price')
def future_electicity_price() -> dict[str,list[dict[str,datetime.datetime|float]]]:
    el_prices = read_future_electicity_price()
    with Session(engine) as session:
        for price in el_prices:
            electricity_price_value = Iot_data(
                name = 'Future Electricity Price',
                value = price.get('electricity_price'),
                inserted_at = price.get('date')
            )
            current_entry = session.query(Iot_data).filter_by(inserted_at = electricity_price_value.inserted_at, name = electricity_price_value.name)
            if not current_entry.first():
                session.add(electricity_price_value)
            else:
                current_entry.update(values = {'value':electricity_price_value.value})
            session.commit()
    print('Stored and/or updated electricty prices!')
    return {"electricy prices":el_prices}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
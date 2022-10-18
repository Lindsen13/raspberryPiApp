from flask import Flask
from sqlalchemy.orm import Session
from utils import read_temperature, construct_engine
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
import os
from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    engine = create_engine(f"mysql+pymysql://{os.environ.get('mysql_user')}:{os.environ.get('mysql_password')}@{os.environ.get('mysql_host')}:{os.environ.get('mysql_port')}?charset=utf8mb4")
    with engine.connect() as conn:
        data = conn.execute("SELECT * FROM tmp.tmp").fetchall()
    return f"Hello world!, {dict(data)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
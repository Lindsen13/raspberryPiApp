from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base
from utils import construct_engine
import datetime

Base = declarative_base()

engine = construct_engine()

class Iot_data(Base):
    __tablename__ = "iot_data"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    value = Column(Float)
    inserted_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"iot_data(id={self.id!r}, name={self.name!r}, value={self.fullname!r})"

if __name__ == '__main__':
    #Iot_data.metadata.drop_all(engine)
    Iot_data.metadata.create_all(engine)
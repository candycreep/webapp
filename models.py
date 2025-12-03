from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = r"sqlite:///C:\Users\worm47\PycharmProjects\PythonProject1\cars_dealers.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Dealer(Base):
    __tablename__ = "dealers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    city = Column(String(100))
    address = Column(String(200))
    area = Column(String(100))
    rating = Column(Float)

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    firm = Column(String(100))
    model = Column(String(100))
    year = Column(Integer)
    power = Column(Integer)
    color = Column(String(50))
    price = Column(Integer)
    dealer_id = Column(Integer, ForeignKey("dealers.id"))
    dealer = relationship("Dealer", back_populates="cars")

Dealer.cars = relationship("Car", back_populates="dealer")


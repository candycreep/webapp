from sqlalchemy.orm import Session
from models import Dealer, Car
import schemas
from event_decorator import EventDecorator

event_decorator = EventDecorator()

def get_dealers(db: Session):
    return db.query(Dealer).all()

def get_dealer(db: Session, dealer_id: int):
    return db.query(Dealer).filter(Dealer.id == dealer_id).first()

def create_dealer(db: Session, dealer: schemas.DealerCreate):
    db_dealer = Dealer(**dealer.dict())
    db.add(db_dealer)
    db.commit()
    db.refresh(db_dealer)
    return db_dealer

def update_dealer(db: Session, dealer_id: int, dealer: schemas.DealerCreate):
    db_dealer = get_dealer(db, dealer_id)
    if db_dealer:
        for key, value in dealer.dict().items():
            setattr(db_dealer, key, value)
        db.commit()
        db.refresh(db_dealer)
    return db_dealer

def delete_dealer(db: Session, dealer_id: int):
    db_dealer = get_dealer(db, dealer_id)
    if db_dealer:
        db.delete(db_dealer)
        db.commit()
    return db_dealer

def get_cars(db: Session):
    return db.query(Car).all()

def get_car(db: Session, car_id: int):
    return db.query(Car).filter(Car.id == car_id).first()

def create_car(db: Session, car: schemas.CarCreate):
    db_car = Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def update_car(db: Session, car_id: int, car: schemas.CarCreate):
    db_car = get_car(db, car_id)
    if db_car:
        for key, value in car.dict().items():
            setattr(db_car, key, value)
        db.commit()
        db.refresh(db_car)
    return db_car
def delete_car(db: Session, car_id: int):
    db_car = get_car(db, car_id)
    if db_car:
        db.delete(db_car)
        db.commit()
    return db_car

create_car = event_decorator.decorate_create(create_car)
update_car = event_decorator.decorate_update(update_car)
delete_car = event_decorator.decorate_delete(delete_car)

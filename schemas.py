from pydantic import BaseModel

class DealerBase(BaseModel):
    name: str
    city: str
    address: str
    area: str
    rating: float

class DealerCreate(DealerBase):
    pass

class Dealer(DealerBase):
    id: int

    class Config:
        from_attributes = True

class CarBase(BaseModel):
    firm: str
    model: str
    year: int
    power: int
    color: str
    price: int
    dealer_id: int

class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int

    class Config:
        from_attributes = True


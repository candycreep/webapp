from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Car Dealers API")

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/dealers/", response_model=list[schemas.Dealer])
def read_dealers(db: Session = Depends(get_db)):
    return crud.get_dealers(db)

@app.get("/dealers/{dealer_id}", response_model=schemas.Dealer)
def read_dealer(dealer_id: int, db: Session = Depends(get_db)):
    dealer = crud.get_dealer(db, dealer_id)
    if dealer is None:
        raise HTTPException(status_code=404, detail="Dealer not found")
    return dealer

@app.post("/dealers/", response_model=schemas.Dealer)
def create_dealer(dealer: schemas.DealerCreate, db: Session = Depends(get_db)):
    return crud.create_dealer(db, dealer)

@app.put("/dealers/{dealer_id}", response_model=schemas.Dealer)
def update_dealer(dealer_id: int, dealer: schemas.DealerCreate, db: Session = Depends(get_db)):
    updated = crud.update_dealer(db, dealer_id, dealer)
    if updated is None:
        raise HTTPException(status_code=404, detail="Dealer not found")
    return updated


@app.delete("/dealers/{dealer_id}")
def delete_dealer(dealer_id: int, db: Session = Depends(get_db)):
    dealer = crud.get_dealer(db, dealer_id)
    if dealer is None:
        raise HTTPException(status_code=404, detail="Dealer not found")

    from models import Car
    car_count = db.query(Car).filter(Car.dealer_id == dealer_id).count()
    if car_count > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete dealer with associated cars. Please transfer the cars to another dealer first."
        )

    crud.delete_dealer(db, dealer_id)
    return {"detail": "Dealer deleted"}

@app.get("/cars/", response_model=list[schemas.Car])
def read_cars(db: Session = Depends(get_db)):
    return crud.get_cars(db)

@app.get("/cars/{car_id}", response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car(db, car_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@app.post("/cars/", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db, car)

@app.put("/cars/{car_id}", response_model=schemas.Car)
def update_car(car_id: int, car: schemas.CarCreate, db: Session = Depends(get_db)):
    updated = crud.update_car(db, car_id, car)
    if updated is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated

@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_car(db, car_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"detail": "Car deleted"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for dev; restrict in prod, e.g., ["http://localhost"])
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)
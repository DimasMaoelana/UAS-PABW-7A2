from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
#
# @app.get("/")
# def root():
#     return cars.db

@app.post("/cars", response_model=schemas.Cars, status_code=status.HTTP_201_CREATED)
def create_cars(cars: schemas.CreateCars, session: Session = Depends(get_session)):

    # create an instance of the ToDo database model
    carsdb = models.Carsku(id = cars.id, brand = cars.brand, model = cars.model, price = cars.price)

    # add it to the session and commit it
    session.add(carsdb)
    session.commit()
    session.refresh(carsdb)

    # return the todo object
    return carsdb

@app.get("/cars/{id}", response_model=schemas.Cars)
def read_cars(id: int, session: Session = Depends(get_session)):

    # get the todo item with the given id
    todo = session.query(models.Carsku).get(id)

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.put("/cars/{id}", response_model=schemas.Cars)
def update_cars(id: int, brand: str, model: str, price: int, session: Session = Depends(get_session)):

    # get the todo item with the given id
    todo = session.query(models.Carsku).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if todo:
        todo.id = id
        session.commit()

        todo.brand = brand
        session.commit()

        todo.model = model
        session.commit()

        todo.price = price
        session.commit()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.delete("/cars/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cars(id: int, session: Session = Depends(get_session)):

    # get the todo item with the given id
    todo = session.query(models.Carsku).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if todo:
        session.delete(todo)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return None

@app.get("/cars", response_model = List[schemas.Cars])
def read_cars_list(session: Session = Depends(get_session)):

    # get all todo items
    cars_list = session.query(models.Carsku).all()

    return cars_list
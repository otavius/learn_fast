from fastapi import FastAPI, Depends, HTTPException
from db import SessionLocal, engine
import models, schemas, service
from db import get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#create user
#get user
#get all users
#create items

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    db_user = service.create_user(db, user)
    return db_user

@app.get("/users", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = service.get_users(db, skip, limit)
    return users 

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = service.create_item(db, item, user_id)
    return item

@app.get("/items", response_model=list[schemas.Item])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_items(db, skip, limit)

@app.get("/users/{user_id}/items", response_model=list[schemas.Item])
def get_items_for_user(user_id: int, db: Session = Depends(get_db)):
    return service.get_items(db, user_id)
    
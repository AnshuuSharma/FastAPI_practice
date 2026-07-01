from fastapi import FastAPI, Depends
from sqlalchemy.orm import session

from database import engine, Base, get_db
import models


from pydantic import BaseModel

app=FastAPI()

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name:str
    age:int

@app.post("/users")
def create_users(user:UserCreate, db:session=Depends(get_db)):
    new_user=models.User(
        name=user.name,
        age=user.age
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



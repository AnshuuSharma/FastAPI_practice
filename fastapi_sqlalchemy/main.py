from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import session

from database import engine, Base, get_db
import models


from pydantic_practice import BaseModel

app=FastAPI()

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name:str
    age:int

class UserUpdate(BaseModel):
    name: str | None = None
    age: int | None = None

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

@app.get("/show")
def get_users(db:session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserCreate,
    db: session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.id == user_id).first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.name = user.name
    existing_user.age = user.age

    db.commit()
    db.refresh(existing_user)

    return existing_user

@app.patch("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.id == user_id).first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.name is not None:
        existing_user.name = user.name

    if user.age is not None:
        existing_user.age = user.age
    db.commit()

    db.refresh(existing_user)

    return existing_user

@app.delete("/remove/{user_id}")
def delete_user(
    user_id:int,
    db:session=Depends(get_db)
):
    user_exists=db.query(models.user).filter(models.user.id==user_id).first()
    if user_exists is None:
        raise HTTPException(status_code=404,detail="user doesn't exixts")
    
    db.delete(user_exists)
    db.commit()

    return {"message":f"user with id : {id} deleted succesfully "}


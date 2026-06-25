from fastapi import FastAPI , HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, List, Dict, Optional


app=FastAPI()

fake_db={}
next_id=1


class CreateUser(BaseModel):
    username:str = Field(max_length=50)
    password:str = Field(min_length=8)

@app.get("/")
def home():
    return {"message":"Hello , welcome to the home page"}

@app.post("/users")
def create_user(user:CreateUser):
    global next_id
    for user in fake_db.values():
        if user["username"]==user.username:
            raise HTTPException(
                status_code=400,
                detail="user already exists"
            )
    
    fake_db[next_id]={
        "username":user.username,
        "password":user.password
    }
    current_id=next_id
    next_id+=1
    
    return {"message":f"user : {user.username} with id : {current_id} created successfully "}

@app.get("/get_user")
def get_user(user_id:int):
    if user_id in fake_db:
        return fake_db[user_id]
    else:
        raise HTTPException(status_code=404, detail="user not found")


@app.put("/modify/")
def modify_user(user_id:int, username:str, password:str):

   if user_id in fake_db.keys():
       fake_db[user_id]["username"]=username
       fake_db[user_id]["password"]=password
       return{"modified successfully"}
   else:
       raise HTTPException(status_code=404, detail="user not found")


@app.delete("/delete/{user_id}")
def delete_user(user_id:int):
    if user_id in fake_db:
        del fake_db[user_id]
        return {"messsage":"user deleted succesfully"}
    else:
        raise HTTPException(status_code=404, detail="user not found")
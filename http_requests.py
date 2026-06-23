from fastapi import FastAPI

app=FastAPI()

fake_db={}
next_id=1

@app.get("/")
def home():
    return {"message":"Hello , welcome to the home page"}

@app.post("/users")
def create_user(username:str,password:str):
    global next_id
    for user in fake_db.values():
        if user["username"]==username:
            return{"error":"user already exists"}
        
    
    fake_db[next_id]={
        "username":username,
        "password":password
    }
    current_id=next_id
    next_id+=1
    
    return {"message":f"user : {username} with id : {current_id} created successfully "}

@app.get("/get_user")
def get_user(user_id:int):
    if user_id in fake_db:
        return fake_db[user_id]
    else:
        return {"error":"user doesnt exists"}


@app.put("/modify/")
def modify_user(user_id:int, username:str, password:str):

   if user_id in fake_db.keys():
       fake_db[user_id]["username"]=username
       fake_db[user_id]["password"]=password
       return{"modified successfully"}
   else:
       return{"error":"user not found"}


@app.delete("/delete/{user_id}")
def delete_user(user_id:int):
    if user_id in fake_db:
        del fake_db[user_id]
        return {"messsage":"user deleted succesfully"}
    else:
        return {"user not found"}
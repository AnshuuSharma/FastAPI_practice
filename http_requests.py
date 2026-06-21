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
    next_id+=1
    
    return {"message":f"user {username} created successfully "}

@app.get("/get_user")
def get_user(username:str):
    for user in fake_db.values():
        if user["username"]==username:
            return{"user":user["username"]}
    else:
        return{"error":"user doesnt exists"}

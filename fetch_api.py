from fastapi import FastAPI
import requests

app=FastAPI()

api=""

@app.get("/api")
def fetch_api():
    response=requests.get("https://jsonplaceholder.typicode.com/posts")

    return response.json()

@app.get("/user/{userId}")
def get_user(userId:str):
    response=requests.get("https://jsonplaceholder.typicode.com/posts",params={"userId":userId})

    if response.status_code!=200:
        return {"error":"couldn't fetch data"}

    return response.json()


@app.get("/even_id")
def get_even_id():
    response=requests.get("https://jsonplaceholder.typicode.com/posts")
    posts=response.json()

    result=[]

    for post in posts:
        try:
            if post["id"]%2==0:
                result.append(post["id"])
        except KeyError:
            continue

    return result
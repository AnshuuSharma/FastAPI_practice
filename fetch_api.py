from fastapi import FastAPI
import requests

app=FastAPI()

api=""

@app.get("/api")
def fetch_api():
    response=requests.get("https://jsonplaceholder.typicode.com/posts")

    return response.json()
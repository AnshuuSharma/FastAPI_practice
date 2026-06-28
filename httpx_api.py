from fastapi import FastAPI
import httpx

app=FastAPI()

@app.get("/users")
async def get_users():
    async with httpx.AsyncClient() as client:
        response=await client.get("https://jsonplaceholder.typicode.com/posts")

    response.raise_for_status()

    return response.json()

@app.get("/user/{userId}")
async def get_user_byId(userId:int):
    async with httpx.AsyncClient() as client:
        response=await client.get("https://jsonplaceholder.typicode.com/posts", params={"userId":userId})

    response.raise_for_status()

    return response.json()
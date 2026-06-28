from fastapi import FastAPI
import httpx

app=FastAPI()

@app.get("/users")
async def get_users():
    async with httpx.AsyncClient() as client:
        response=await client.get("https://jsonplaceholder.typicode.com/posts")

    response.raise_for_status()

    return response.json()
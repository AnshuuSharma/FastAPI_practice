from fastapi import FastAPI, HTTPException
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

@app.post("/user/data")
async def create_post():
    async with httpx.AsyncClient() as client:
        response=await client.post("https://jsonplaceholder.typicode.com/posts", json={
            "userId":10,"id":101,"title":"hello world","body":"quia sjhfoh suscipit\nsuscipit  consequuntur et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
        })

        response.raise_for_status()

    return response.json()

@app.put("/update")
async def update_post(id:int):
    async with httpx.AsyncClient() as client:
        response=await client.put(f"https://jsonplaceholder.typicode.com/posts/{id}", 
            json={
                "userId": 1,
                "title": "New Title",
                "body": "New Body"
        })
        response.raise_for_status()
    return response.json()

@app.patch("/posts/{id}")
async def update_using_patch(id:int):
    async with httpx.AsyncClient() as client:
        response=await client.patch(f"https://jsonplaceholder.typicode.com/posts/{id}", 
            json={"title":"updated title"}
                
                )
        response.raise_for_status()
    return response.json()

@app.delete("/remove/{id}")
async def delete_post(id:int):
    try:
        async with httpx.AsyncClient() as client:
           response=await client.delete(f"https://jsonplaceholder.typicode.com/posts/{id}")
           response.raise_for_status()
        return {"message":{f"post with {id} succesfully deleted"}}
    except HTTPException as e:
        return{"error":e}


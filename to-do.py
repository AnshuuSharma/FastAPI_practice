from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple To-Do API")

class Todo(BaseModel):
    title: str
    completed: bool = False

todos: list[Todo] = []


@app.get("/")
def home():
    return {"message": "Welcome to the To-Do API. Visit /docs to try it out."}


@app.get("/todos")
def get_todos():
    return todos


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id < 0 or todo_id >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]


@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    todos.append(todo)
    return {"id": len(todos) - 1, "todo": todo}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    if todo_id < 0 or todo_id >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = updated_todo
    return {"id": todo_id, "todo": updated_todo}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id < 0 or todo_id >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    deleted = todos.pop(todo_id)
    return {"message": "Deleted", "todo": deleted}
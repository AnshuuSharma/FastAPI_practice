from fastapi import FastAPI
from database import conn, cursor

app=FastAPI()

@app.post("/users")
def create_user():

    cursor.execute(
        """
        INSERT INTO users(name,age)
        VALUES (?,?)
        """
        ("Anshu",22)
    )
    conn.commit()

    return {
        "message" : "user created"
    }

@app.get("/users")
def get_users():

    cursor.execute(
        "SELECT * FROM users"
    )

    users=cursor.fetchall()

    return users
# Challenge: Admin Dashboard Access Control

# You are building an internal admin dashboard API for a company. Some endpoints should only be accessible by administrators, so you want to avoid repeating the same role-checking logic in every endpoint. Create a reusable dependency function called verify_admin that checks a request header named role. If the role is "admin", the request should continue. If the role is anything else, the dependency should stop the request and return a 403 Forbidden error with the message "Admin access required". Then create a GET /dashboard endpoint that uses this dependency. If the user is an admin, the endpoint should return a JSON response saying "Welcome to admin dashboard".

from fastapi import FastAPI,Depends,Header,HTTPException

app=FastAPI()

def verify_admin(role:str=Header(...)):
    if role!="admin":
        raise HTTPException(
            status_code=403,
            detail="admin access required"
        )

@app.get("/dashboard")
def dashboard(_:None=Depends(verify_admin)):
    return{"message":"Welcome to admin dashboard"}
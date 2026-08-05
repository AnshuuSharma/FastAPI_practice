# Challenge: The "Inventory Management" APIScenario: You are building an endpoint to restock inventory items. The endpoint must accept an item ID and a list of new stock batch entries. It must calculate the total new quantity, validate data boundaries, and return a structured summary.Your Task :
# Write a POST /inventory/{item_id}/restock endpoint that meets these requirements:
# Path Parameter: item_id (must be a positive integer greater than 0).
# Request Body: A JSON array containing batch objects. 
# Each batch object has:supplier_name (string, minimum 3 characters)quantity (integer, must be greater than 0)
# Business Logic & Validation:If the item_id is greater than 999, raise an HTTP 404 Not Found with the detail message "Item profile does not exist".
# Sum up the total quantity across all submitted batches.Expected Output: Return a JSON response with status code 200 OK matching this structure:json{
#   "item_id": 42,
#   "total_batches_added": 2,
#   "total_quantity_added": 150,
#   "status": "completed"
# }


from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import List

class BatchObjects(BaseModel):
    supplier_name:str=Field(...,min_length=3)
    quantity:int=Field(...,gt=0)

class SummaryResponse(BaseModel):
    item_id:int
    total_batches_added:int
    total_quantity_added:int
    status:str

app=FastAPI()

@app.post("/inventory/{item_id}/restock",response_model=SummaryResponse)
def restock_summary(batches:List[BatchObjects], item_id:int=Path(..., gt=0)):
    if item_id>99:
        raise HTTPException(status_code=404,detail="Item profile does not exist")
    
    batches_added=len(batches)
    quantity=sum(batch.quantity for batch in batches)

    return {"item_id":item_id,
            "total_batches_added":batches_added,
            "total_quantity_added":quantity,
            "status":"completed"
            }



# Challenge: The "Order Discount" API
# Scenario: You're building an endpoint for an e-commerce system that applies discount codes to an order and returns a price breakdown.
# Your Task:
# Write a POST /orders/{order_id}/apply-discount endpoint that meets these requirements:

# Path Parameter: order_id (must be a positive integer greater than 0)
# Request Body: A JSON object with:

# discount_code (string, must be exactly 6 characters)
# items — a list of item objects, each with:

# product_name (string, minimum 2 characters)
# price (float, must be greater than 0)
# quantity (integer, must be greater than 0)

# If order_id is greater than 9999, raise an HTTP 404 Not Found with detail "Order not found".
# Calculate subtotal = sum of (price * quantity) across all items.
# If discount_code starts with "SAVE10", apply a 10% discount to the subtotal. Otherwise, apply 0% discount.
# Return a 200 OK response matching this structure:

# json{
#   "order_id": 101,
#   "subtotal": 500.0,
#   "discount_applied": 50.0,
#   "final_total": 450.0,
#   "status": "discount_applied"
# }

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import List

app=FastAPI()

class Items(BaseModel):
    product_name:str=Field(min_length=2)
    price:float=Field(gt=0)
    quantity:int=Field(gt=0)

class ApplyDiscountReq(BaseModel):
    discount_code:str=Field(...,min_length=6,max_length=6)
    items:List[Items]


@app.post("/orders/{order_id}/apply-discount",status_code=200)
def apply_discount(discount:ApplyDiscountReq,order_id:int=Path(...,gt=0)):
    if order_id>9999:
        raise HTTPException(status_code=404, detail="order not found")
    
    subtotal=sum(obj.price*obj.quantity for obj in discount.items)
    
    if discount.discount_code.startswith("SAVE10"):
        final_total=subtotal*0.9
    else:
        final_total=subtotal
    return {
        "order_id":order_id,
        "subtotal":subtotal,
        "discount_applied":subtotal-final_total,
        "final_total":final_total,
        "status":"discount_applied"
    }
    

# Challenge: The "Employee Leave Request" API
# Scenario: You're building an endpoint for an HR system where employees submit leave requests, and the system checks eligibility and returns a decision.
# Your Task:
# Write a POST /employees/{employee_id}/leave-request endpoint that meets these requirements:

# Path Parameter: employee_id (must be a positive integer greater than 0)
# Request Body: A JSON object with:

# leave_type (string, must be one of: "sick", "casual", "earned") — no need to use Enum, just validate manually
# start_date (string, format "YYYY-MM-DD")
# end_date (string, format "YYYY-MM-DD")
# reason (string, minimum 10 characters)
# If employee_id is greater than 500, raise HTTP 404 Not Found with detail "Employee not found".
# If leave_type is not one of the three allowed values, raise HTTP 400 Bad Request with detail "Invalid leave type".
# Calculate total_days = number of days between start_date and end_date (inclusive of both dates).
# If total_days is greater than 15, raise HTTP 400 Bad Request with detail "Leave duration exceeds maximum allowed limit".
# If everything is valid, return 200 OK:

# json{
#   "employee_id": 12,
#   "leave_type": "sick",
#   "total_days": 4,
#   "status": "approved"
# }

from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, BeforeValidator, Field
from typing import Literal, Annotated
from datetime import datetime,date


def DateFormat(value:str) ->date:
    return datetime.strptime(value,"%Y-%m-%d").date()

FormatDate=Annotated[date,BeforeValidator(DateFormat)]

class LeaveReq(BaseModel):
    leave_type:Literal["sick","casual","earned"] 
    start_date:FormatDate
    end_date:FormatDate
    reason:str=Field(min_length=10)


app=FastAPI()

@app.post("/employees/{employee_id}/leave-request", status_code=200)
def leave_approval(leave:LeaveReq,employee_id:int=Path(...,gt=0)):
    if employee_id>500:
        raise HTTPException(status_code=404,detail="employee not found")
    
    total_days=leave.end_date-leave.start_date
    total_days=total_days.days+1

    if total_days>15:
        raise HTTPException(status_code=400,detail="Leave duration exceeds maximum allowed limit")
    
    return{
        "employee_id":employee_id,
        "leave_type":leave.leave_type,
        "total_days":total_days,
        "status":"approved"
    }
    
# Your Task:
# Implement these three endpoints for managing tasks (assume an in-memory Python dict tasks_db = {} as your "database", where key = task_id and value = task details):
# 1. POST /tasks

# Request body: title (string, min 3 chars), priority (string, one of "low", "medium", "high")
# Auto-generate a task_id (just use len(tasks_db) + 1 for simplicity)
# Save it into tasks_db with a default status of "pending"
# Return 201 Created with the full task object (including task_id)

# 2. GET /tasks/{task_id}

# If task_id doesn't exist in tasks_db, raise 404 Not Found with detail "Task not found"
# Otherwise return the task, 200 OK

# 3. PUT /tasks/{task_id}/status

# Request body: status (string, must be one of "pending", "in_progress", "completed")
# If task_id doesn't exist, raise 404 Not Found
# Update the task's status in place in tasks_db
# Return the updated task, 200 OK

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Literal

app=FastAPI()

tasks_db={}

class TaskReq(BaseModel):
    title:str=Field(min_length=3)
    priority:Literal["low","medium","high"]

class UpdateReq(BaseModel):
    status:Literal["pending","in_progress","completed"]


@app.post("/tasks")
def create_task(task:TaskReq):
    task_id=len(tasks_db)+1

    tasks_db[task_id]={
        "task_id":task_id, 
        "title":task.title,
        "priority":task.priority,
        "status":"pending"
    }

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=tasks_db[task_id]
    )

@app.get("/tasks/{task_id}")
def get_tasks(task_id:int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="task not found")
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=tasks_db[task_id]
    )


@app.put("/tasks/{task_id}/status")
def update_task(task_id:int, get_status:UpdateReq):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404,detail="task not found")
    
    tasks_db[task_id]["status"]=get_status.status

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=tasks_db[task_id]
    )


    
# Challenge: The "GitHub Repo Filter" API
# Scenario: You're building an endpoint that fetches a GitHub user's public repositories and returns only the ones matching certain criteria — a common real-world pattern (call external API → filter/transform → return your own shape).
# Your Task:
# Write a GET /github/{username}/popular-repos endpoint that:

# Path Parameter: username (string)
# Query Parameter: min_stars (int, default 10) — only return repos with stargazers_count >= min_stars

# Logic:

# Call the GitHub public API: https://api.github.com/users/{username}/repos using the requests (or httpx) library. This returns a JSON array of repo objects (each has fields like name, stargazers_count, language, html_url, etc.)
# If the GitHub API returns a 404 (user doesn't exist), raise your own HTTPException with 404 and detail "GitHub user not found".
# Filter the repos to only those where stargazers_count >= min_stars.
# Sort the filtered repos by stargazers_count in descending order.
# Return a JSON response shaped like:

# json{
#   "username": "torvalds",
#   "total_matching_repos": 3,
#   "repos": [
#     {"name": "linux", "stars": 190000, "language": "C", "url": "https://github.com/torvalds/linux"}
#   ]
# }

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx

app=FastAPI()

class UserReq(BaseModel):
    name:str


@app.get("/github/{username}/popular-repos")
async def get_repos(username:str, min_stars:int=10):
    try:
        async with httpx.AsyncClient() as client:
            response=await client.get(f"https://api.github.com/users/{username}/repos")
            response.raise_for_status()

            data=response.json()

            result=[]

            for obj in data:
                if obj["stargaze_count"]>=min_stars:
                    result.append(obj)

            return JSONResponse(
                content={
                    "username":username,
                    "total_matching_Records":len(result),
                    "repos":sorted(result,key=lambda repo:repo["stargaze_count"],reverse=True)
            }
        )
    except HTTPException as e:
        if e.response.status_code==404:
            raise HTTPException(status_code=404,detail="Github user not found")
        raise HTTPException(status_code=502,detail="error contacting github")


        



# Challenge : Weather Aggregator API
# Scenario

# You're building the backend for a travel application.

# Instead of exposing the raw weather API response, your backend should fetch the data, extract only what's needed, and return a clean response.

# Your Task

# Create

# GET /weather/{city}
# Path Parameter
# city: str
# Query Parameter
# unit: str = "celsius"

# Allowed values:

# celsius
# fahrenheit

# If anything else is passed, return 400 Bad Request.

# Use this endpoint:

# https://wttr.in/{city}?format=j1

# If the API request fails (timeout, network issue), return
# 503 Service Unavailable

# with

# "Weather service unavailable"
# Extract only
# city
# current temperature
# humidity
# weather description
# feels like temperature
# If
# unit=fahrenheit

# return Fahrenheit values.

# Otherwise return Celsius.

# Expected Response
# {
#     "city": "London",
#     "temperature": 21,
#     "feels_like": 23,
#     "humidity": 62,
#     "description": "Partly cloudy",
#     "unit": "celsius"
# }


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app=FastAPI()

class weatherResponse(BaseModel):
    city:str
    temperature:int
    feels_like:int
    humidity:int
    description:str
    unit:str

@app.get("/weather/{city}",response_model=weatherResponse, status_code=200)
async def get_details(city:str, unit:str="celsius"):
    try:
        if unit not in ["celsius","fahrenheit"]:
          raise HTTPException(status_code=400,detail="Bad request : only celsius and fahrenheit unit is accepted")
        async with httpx.AsyncClient(timeout=5.0) as client:
         response=await client.get(f"https://wttr.in/{city}", params={"format":"j1"})

         response.raise_for_status()

         data=response.json()

         if not data.get("current_condition"):
            raise HTTPException(status_code=404, detail="City not found")
         result={}
         result["city"]=data["nearest_area"][0]["areaName"][0]["value"]
         result["temperature"]=data["current_condition"][0]["temp_C"] if unit=="celsius" else data[ "current_condition"][0]["temp_F"]
                
         result["feels_like"]=data["current_condition"][0]["FeelsLikeC"] if unit=="celsius" else data[ "current_condition"][0]["FeelsLikeF"]
         result["humidity"]=data["current_condition"][0]["humidity"]
         result["description"]=data["current_condition"][0]["weatherDesc"][0]["value"]  
         result["unit"]=unit

         return result
     
    except httpx.RequestError:
         raise HTTPException(status_code=503, detail="Weather service unavailable")

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=503,
            detail="Weather service unavailable"
        )


# Challenge 6: URL Shortener API
# Scenario

# You're building the backend for a URL shortening service (similar to Bitly).

# The application stores mappings between a short code and the original URL.

# Assume you're using SQLAlchemy ORM and already have a URL table with these columns:

# id
# original_url
# short_code
# created_at

# You don't need to write the model or database setup—just the FastAPI endpoint.

# Your Task

# Create:

# POST /shorten
# Request Body
# {
#     "url": "https://fastapi.tiangolo.com/tutorial/"
# }
# Logic
# Validate that the URL is a valid HTTP or HTTPS URL using Pydantic.
# Generate a random 6-character alphanumeric short_code.

# Example:

# aB91xZ
# Before saving, check if that short_code already exists in the database.
# If it exists, generate another one.
# Keep trying until you get a unique code.
# Save the record in the database.
# Return:
# {
#     "short_code": "aB91xZ",
#     "short_url": "http://localhost:8000/aB91xZ",
#     "original_url": "https://fastapi.tiangolo.com/tutorial/"
# }


from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, AnyHttpUrl
from sqlalchemy.orm import Session
import random
import string

from database import get_db
import models

app = FastAPI()


class ApiRequest(BaseModel):
    url: AnyHttpUrl


@app.post("/shorten", status_code=201)
def url_shortener(request: ApiRequest, db: Session = Depends(get_db)):
    characters = string.ascii_letters + string.digits

    try:
        while True:
            short_code = "".join(random.choices(characters, k=6))

            existing_code = (
                db.query(models.URLs)
                .filter(models.URLs.short_code == short_code)
                .first()
            )

            if not existing_code:
                break

        new_url = models.URLs(
            original_url=str(request.url),
            short_code=short_code,
        )

        db.add(new_url)
        db.commit()
        db.refresh(new_url)

        return {
            "short_code": new_url.short_code,
            "short_url": f"http://localhost:8000/{new_url.short_code}",
            "original_url": new_url.original_url,
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create short URL",
        )



# Challenge 7: Resume Upload API
# Scenario

# You're building the backend for an AI Resume Analyzer.

# Users upload their resumes, and your API stores them before they are processed by an AI model.

# Your Task

# Create:

# POST /upload-resume
# Request

# Accept:

# A PDF file
# Form field:
# candidate_name (string)

# Use:

# UploadFile
# File
# Form
# Logic
# Accept only PDF files.
# Reject files larger than 2 MB.
# Save the file inside an uploads/ directory.
# Rename the file as:
# <candidate_name>.pdf

# Example:

# uploads/Anshu.pdf
# If a file with the same name already exists, overwrite it.
# Response
# {
#     "message": "Resume uploaded successfully",
#     "filename": "Anshu.pdf",
#     "size": 154321
# }

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload-resume")
async def upload_resume(
    candidate_name: str = Form(...),
    file: UploadFile = File(...)
):
    # Validate content type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    content = await file.read()

    # Validate size (2 MB)
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds 2 MB"
        )

    filename = f"{candidate_name}.pdf"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # Save (overwrites if exists)
    with open(filepath, "wb") as f:
        f.write(content)

    return {
        "message": "Resume uploaded successfully",
        "filename": filename,
        "size": len(content)
    }


# Challenge 8: Product Catalog API
# Scenario

# You're building an e-commerce backend.

# The database already contains a Product table.

# id
# name
# category
# price
# stock

# You don't need to create the model.

# Your Task

# Create

# GET /products
# Query Parameters
# Parameter	Type	Default
# category	str	None
# min_price	float	None
# max_price	float	None
# in_stock	bool	False
# sort_by	str	"price"
# order	str	"asc"
# page	int	1
# limit	int	10
# Logic
# If category is provided, return only that category.
# If min_price is provided, return products whose price is >= min_price.
# If max_price is provided, return products whose price is <= max_price.
# If in_stock=true, return only products where stock > 0.
# Allow sorting by:
# price
# name

# If any other field is provided,

# return

# 400 Bad Request
# Support
# ?page=2&limit=5

# using SQL pagination.
# Expected Response
# {
#     "page": 2,
#     "limit": 5,
#     "total": 18,
#     "products": [
#         {
#             "id": 12,
#             "name": "MacBook Air",
#             "price": 89000,
#             "stock": 6
#         }
#     ]
# }


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models

app = FastAPI()


@app.get("/products")
def get_products(
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    in_stock: bool = False,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):

    query = db.query(models.Product)

    # Filtering
    if category:
        query = query.filter(models.Product.category == category)

    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)

    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    if in_stock:
        query = query.filter(models.Product.stock > 0)

    # Sorting
    if sort_by not in ["price", "name"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    column = getattr(models.Product, sort_by)

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    total = query.count()

    products = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "products": products
    }


# Challenge 9: Random User API
# Scenario

# You're building a simple API for an HR application.

# Instead of exposing the full response from an external API, your endpoint should return only the required fields.

# Your Task

# Create:

# GET /random-user
# Query Parameter
# nationality (optional)

# Example:

# GET /random-user?nationality=us
# External API

# Call:

# https://randomuser.me/api/

# If nationality is provided:

# https://randomuser.me/api/?nat=us
# Logic
# Fetch one random user using httpx.AsyncClient.
# If the external API is unavailable, return
# 503 Service Unavailable
# {
#     "detail": "Random User service unavailable"
# }
# Return only these fields:
# Full Name
# Email
# Country
# Age
# Profile Picture
# Expected Response
# {
#     "name": "John Smith",
#     "email": "john.smith@example.com",
#     "country": "United States",
#     "age": 32,
#     "profile_picture": "https://randomuser.me/api/portraits/men/75.jpg"
# Bonus

# Validate that nationality, if provided, is one of:

# us
# gb
# in
# ca
# au

# Otherwise return

# 400 Bad Request


from fastapi import FastAPI, HTTPException
from typing import Literal
import httpx

app = FastAPI()


@app.get("/random-user")
async def get_random_user(
    nationality: Literal["us", "gb", "in", "ca", "au"] | None = None
):
    params = {}

    if nationality:
        params["nat"] = nationality

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://randomuser.me/api/",
                params=params
            )

            response.raise_for_status()

            data = response.json()

            user = data["results"][0]

            return {
                "name": f"{user['name']['first']} {user['name']['last']}",
                "email": user["email"],
                "country": user["location"]["country"],
                "age": user["dob"]["age"],
                "profile_picture": user["picture"]["large"],
            }

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=503,
            detail="Random User service unavailable"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Random User service unavailable"
        )


# Challenge 10: Quote of the Day API
# Scenario

# Your team is building a motivational dashboard for employees. Every time the frontend loads, it should display a random inspirational quote. Instead of letting the frontend directly call a third-party API, your backend should fetch the quote, extract only the necessary information, and return a simplified response. This way, if the external API changes in the future, only your backend needs to be updated.

# Create a GET endpoint named /quote. Your endpoint should fetch a random quote from the following API:

# https://dummyjson.com/quotes/random

# The external API returns several fields, but your API should return only:

# quote
# author
# length of the quote (number of characters)

# If the external API is unavailable or the request fails, return:

# 503 Service Unavailable

# with the message:

# {
#     "detail": "Quote service unavailable"
# }

# The expected response from your API should look like:

# {
#     "quote": "The best way to predict the future is to create it.",
#     "author": "Peter Drucker",
#     "length": 47
# }

from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()


@app.get("/quote")
async def get_quote():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://dummyjson.com/quotes/random"
            )

            response.raise_for_status()

            data = response.json()

            return {
                "quote": data["quote"],
                "author": data["author"],
                "length": len(data["quote"])
            }

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=503,
            detail="Quote service unavailable"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Quote service unavailable"
        )

# Challenge 11: Currency Converter API

# You are building a simple currency conversion service for a travel application. Instead of maintaining exchange rates yourself, your backend should fetch the latest exchange rates from an external API and calculate the converted amount. Create a GET endpoint /convert that accepts three query parameters: from_currency, to_currency, and amount. Use the external API:

# https://open.er-api.com/v6/latest/{from_currency}

# The API returns exchange rates for the given base currency. Your task is to retrieve the exchange rate for to_currency, multiply it by the given amount, and return a simplified JSON response containing the original amount, source currency, destination currency, exchange rate, and converted amount.

# If the source or destination currency is invalid, return a 400 Bad Request with the message "Invalid currency code". If the external API is unavailable or the request fails, return 503 Service Unavailable with the message "Currency service unavailable".

# For example, if the request is:

# GET /convert?from_currency=USD&to_currency=INR&amount=100

# Your response should look similar to:
# {
#     "from_currency": "USD",
#     "to_currency": "INR",
#     "amount": 100,
#     "exchange_rate": 87.45,
#     "converted_amount": 8745.0
# }


from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()


@app.get("/convert")
async def convert_currency(
    from_currency: str,
    to_currency: str,
    amount: float
):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
            )

            response.raise_for_status()

            data = response.json()

            if data.get("result") != "success":
                raise HTTPException(
                    status_code=400,
                    detail="Invalid currency code"
                )

            rates = data["rates"]

            if to_currency.upper() not in rates:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid currency code"
                )

            exchange_rate = rates[to_currency.upper()]
            converted_amount = amount * exchange_rate

            return {
                "from_currency": from_currency.upper(),
                "to_currency": to_currency.upper(),
                "amount": amount,
                "exchange_rate": exchange_rate,
                "converted_amount": round(converted_amount, 2)
            }

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=503,
            detail="Currency service unavailable"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Currency service unavailable"
        )


# Challenge 12: Age Predictor API

# You are building a small utility service for a recruitment platform. The frontend sends a person's first name, and your backend should estimate their age using a public API. Instead of returning the complete response from the external service, your API should return only the information the frontend needs. Create a GET endpoint called /predict-age that accepts a query parameter named name. Use the external API:

# https://api.agify.io/?name=<name>

# The external API returns data similar to:

# {
#     "count": 15432,
#     "name": "john",
#     "age": 42
# }

# Your endpoint should return only:

# {
#     "name": "john",
#     "predicted_age": 42,
#     "message": "Estimated age generated successfully"
# }

from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()


@app.get("/predict-age")
async def predict_age(name: str):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://api.agify.io/",
                params={"name": name}
            )

            response.raise_for_status()

            data = response.json()

            return {
                "name": data["name"],
                "predicted_age": data["age"],
                "message": "Estimated age generated successfully"
            }

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=503,
            detail="Age prediction service unavailable"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Age prediction service unavailable"
        )



# Challenge 13

# You are building a movie recommendation service for a streaming platform. Create a GET endpoint /movie/{title} that accepts a movie title as a path parameter and fetches its details from the OMDb API using the URL https://www.omdbapi.com/?t={title}&apikey=YOUR_API_KEY. If the movie exists, return only the movie's title, year, genre, IMDb rating, and director in a custom JSON response. If the movie is not found, return a 404 Not Found response with the message "Movie not found". If the external API cannot be reached or returns an error, return a 503 Service Unavailable response with the message "Movie service unavailable".

# Note: Replace YOUR_API_KEY with your own OMDb API key.

from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

API_KEY = "YOUR_API_KEY"


@app.get("/movie/{title}")
async def get_movie(title: str):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://www.omdbapi.com/",
                params={
                    "t": title,
                    "apikey": API_KEY
                }
            )

            response.raise_for_status()

            data = response.json()

            if data.get("Response") == "False":
                raise HTTPException(
                    status_code=404,
                    detail="Movie not found"
                )

            return {
                "title": data["Title"],
                "year": data["Year"],
                "genre": data["Genre"],
                "imdb_rating": data["imdbRating"],
                "director": data["Director"]
            }

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=503,
            detail="Movie service unavailable"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Movie service unavailable"
        )
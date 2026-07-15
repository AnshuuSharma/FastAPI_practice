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


    

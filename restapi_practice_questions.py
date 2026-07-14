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
    


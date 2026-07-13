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

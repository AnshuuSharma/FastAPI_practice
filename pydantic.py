from pydantic import basemodel, field, emailstr, anyurl
from typing import list, Dict, Optional, Annotated

class Developer(basemodel):
    name:str=field(max_length=50),
    age:int=field(gt=0,lt=120),
    hobbies:Optional[list[str]]=field(max_length=5)
    email:emailstr
    github:anyurl


    


    
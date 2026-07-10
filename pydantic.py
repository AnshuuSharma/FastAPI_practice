from pydantic import basemodel, Field, emailstr, anyurl
from typing import list, Dict, Optional, Annotated , field_validator


class Developer(basemodel):
    name:str=Field(max_length=50),
    age:int=Field(gt=0,lt=120),
    hobbies:Optional[list[str]]=Field(max_length=5)
    email:emailstr
    github:anyurl

#------- Add Metadata -----------
class Developer(basemodel):
    name: Annotated[str, Field(max_length=20, 
                               title="name of the developer " ,
                               description="write the name of the developer in less than 20 characters ",
                               examples=["John","Jenny"]
                               )]
    age:int=Field(gt=0,lt=120),
    hobbies:Annotated[Optional[list[str]], Field(default=None, max_length=20)]
    email:emailstr
    github:anyurl
    weight:Annotated[float,Field(gt=0,strict=True)]


class Person(basemodel):
    email:emailstr

@field_validator('email')
@classmethod
def email_validator(cls,value):
    valid_domains=['gmail.com']
    domain_name=value.split('@')[1]


    if domain_name not in valid_domains:
        raise ValueError('not a valid domain')
    return value



    
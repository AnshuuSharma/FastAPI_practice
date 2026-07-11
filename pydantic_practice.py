from typing import List, Dict, Optional, Annotated

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    AnyUrl,
    field_validator,
    model_validator,
)


class Developer(BaseModel):
    name:str=Field(max_length=50),
    age:int=Field(gt=0,lt=120),
    hobbies:Optional[list[str]]=Field(max_length=5)
    email:EmailStr
    github:AnyUrl

#------- Add Metadata -----------
class Developer(BaseModel):
    name: Annotated[str, Field(max_length=20, 
                               title="name of the developer " ,
                               description="write the name of the developer in less than 20 characters ",
                               examples=["John","Jenny"]
                               )]
    age:int=Field(gt=0,lt=120),
    hobbies:Annotated[Optional[List[str]], Field(default=None, max_length=20)]
    email:EmailStr
    github:AnyUrl
    weight:Annotated[float,Field(gt=0,strict=True)]


class Person(BaseModel):
    email:EmailStr

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['gmail.com']
        domain_name=value.split('@')[1]


        if domain_name not in valid_domains:
            raise ValueError('not a valid domain')
        return value

person = Person(email="abc@gmail.com")
print(person)

class User(BaseModel):
    age:int
    contact_details:dict[str,str]

    @model_validator(mode='after')
    def validate_contact(self):
        if self.age>70 and 'emergency' not in self.contact_details:
            raise ValueError('patients older than 70 must have emergency contact')
        
        return self
    
user = User(
    age=75,
    contact_details={
        "emergency": "9876543210"
    }
)

print(user)
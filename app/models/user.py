from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, lt=120)
    password: str
    email: Optional[str] = None

class UserResponse(BaseModel):
    name: str
    age: int

'''
[MinLength(2)]
[MaxLength(50)]
public string Name { get; set; }

[Range(1, 119)]
public int Age { get; set; }

public string? Email { get; set; }
'''
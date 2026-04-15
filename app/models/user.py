from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, lt=120)
    #password: str
    #email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    model_config = ConfigDict(from_attributes=True)
    '''
    It tells Pydantic:
    “You can read data from object attributes, not just dicts”
    return new UserDto { Name = user.Name }; -> automatically
    '''

'''
[MinLength(2)]
[MaxLength(50)]
public string Name { get; set; }

[Range(1, 119)]
public int Age { get; set; }

public string? Email { get; set; }
'''
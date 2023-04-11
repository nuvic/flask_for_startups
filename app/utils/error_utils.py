# Standard Library imports

# Core Flask imports

# Third-party imports
from pydantic import BaseModel, validator, constr, EmailStr

# App imports


class AccountValidator(BaseModel):
    username: constr(min_length=1, max_length=15) = ...
    email: EmailStr = ...
    password: str = ...

    @validator('username')
    def username_valid(cls, v):
        if not v[0].isalpha():
            raise ValueError('Username must start with a letter')
        if not v.isalnum():
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v

class EmailValidator(BaseModel):
    email: EmailStr

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime  # <-- Added import here to define the type


class SignUpIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    # FIX: Change type hint from 'str' to 'datetime'
    created_at: datetime 
    
    class Config:
        from_attributes = True

class PasswordResetRequestIn(BaseModel):
    email: EmailStr

class PasswordResetIn(BaseModel):
    token: str
    new_password: str
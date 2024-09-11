from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class FileUpload(BaseModel):
    filename: str
    content: bytes

class TokenData(BaseModel):
    username: Optional[str] = None

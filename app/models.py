from pydantic import BaseModel,EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class PromptRequest(BaseModel):
    prompt: str

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str
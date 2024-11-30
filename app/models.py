from pydantic import BaseModel,EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class PromptRequest(BaseModel):
    prompt: str
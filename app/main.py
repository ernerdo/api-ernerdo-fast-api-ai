from fastapi import FastAPI, HTTPException
from .supa_config import supabase_client
from .models import LoginUser


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI with Docker!"}

@app.post("/login")
async def login(user: LoginUser):
    try:
        response = supabase_client.auth.sign_in_with_password(
            {"email": user.email, "password": user.password}
        )
        
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": {
                "id": response.user.id,
                "email": response.user.email,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/logout")
async def logout():
    try:
        response = supabase_client.auth.sign_out()
        
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(ec))
    
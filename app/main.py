from fastapi import FastAPI, HTTPException
from .supa_config import supabase_client
from .models import LoginRequest, PromptRequest
from .open_ai import open_ai_client


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI with Docker!"}

@app.post("/login")
async def login(request: LoginRequest):
    try:
        response = supabase_client.auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
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

@app.post("/ask")
async def ask(request: PromptRequest):
    try:
        response = open_ai_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": request.prompt
                }
            ]
        )

        supabase_client.table("chat_history").insert({
            "prompt": request.prompt,
            "response": response.choices[0].message.content,
            "model": "gpt-4o-mini",
            "is_success": 1
        }).execute()
        
        return response.choices[0].message.content
    except Exception as e:
        supabase_client.table("chat_history").insert({
            "prompt": request.prompt,
            "error_message": str(e),
            "model": "gpt-4o-mini",
            "is_success":0,
        }).execute()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/history")
async def history():
    try:
        response = supabase_client.table("chat_history").select("*").execute()
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
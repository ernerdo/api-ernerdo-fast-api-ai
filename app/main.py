from fastapi import FastAPI, HTTPException, Depends, Request
from .supa_config import supabase_client
from .models import LoginRequest, PromptRequest
from .open_ai import open_ai_client
from .auth import authenticate_user

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://ai-app.ernerdo.xyz/"],  # Dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ask",dependencies=[Depends(authenticate_user)])
async def ask(request: Request,body: PromptRequest):
    try:
        response = open_ai_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": body.prompt
                }
            ]
        )
        ai_response = response.choices[0].message.content
    except Exception as openai_error:
        supabase_client.table("chat_history").insert({
            "prompt": body.prompt,
            "error_message": str(openai_error),
            "model": "gpt-4o-mini",
            "is_success": 0,
            "user_id": request.state.user_id
        }).execute()
        raise HTTPException(status_code=500, detail="Error with OpenAI service.")
    

    supabase_client.table("chat_history").insert({
        "prompt": body.prompt,
        "response": ai_response,
        "model": "gpt-4o-mini",
        "user_id": request.state.user_id
    }).execute()
    
    return ai_response


@app.get("/history",dependencies=[Depends(authenticate_user)])
async def history(request: Request):
    try:
        user_id = request.state.user_id
        print("user_id: ", user_id)
        response = supabase_client.table("chat_history").select("*").execute()
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
from fastapi import Request, HTTPException
from .supa_config import supabase_client


async def authenticate_user(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        auth = supabase_client.auth.get_user(token)
        
        if not auth or not auth.user:
            raise HTTPException(status_code=401, detail="Invalid user token")
        request.state.user_id = auth.user.id

    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid user token")


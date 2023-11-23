import jwt
from fastapi import FastAPI,HTTPException,APIRouter
import time
from decouple import config
from mongo_db import *
import hashlib
from models import *
import fastapi
import uuid

router = APIRouter()

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def token_resp(token: str):
    return {
        "access_token": token
    }

def signJWT(userId: str):
    expiration_time = time.time() + 600
    print("userId",userId)
    try:
        user_id = userId.decode()
    except Exception as e:
        user_id = userId
    payload = {
        "userId": user_id,
        "exp": expiration_time
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(token_resp(token))
    return token_resp(token)

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print("decoded_token",decoded_token)
        exp_claim = decoded_token.get('exp')
        
        if exp_claim is None:
            return {"error": "'exp' claim is missing in the token"}
        
        return decoded_token if exp_claim >= time.time() else None
    except:
        return {"error": "Token has expired"}
    
async def check_user(data):
    passwo = hashlib.md5(data.password.encode('utf-8')).hexdigest()
    collection = await connect_collection("Users","users")
    result = collection.find_one({"email": data.username})
    if result.get("email") == data.username and result.get("password") == passwo:
        return True
    else:
        return False
    
@router.post("/login", tags=['Authentication'])
async def verification(request: verify_params):
    cookie_name = "Akhil"
    if check_user(request):
        cookie_id = str(uuid.uuid4())
        print("cookie_id",cookie_id)
        access_token =  signJWT(request.username)
        redis_client = redisclient()
        store_cookie_id = redis_client.redis_client.hset("CookieStore", cookie_id, "useraccesstoken." + access_token["access_token"])
        response = fastapi.responses.JSONResponse({"status": "Logged in Successfully","token" : access_token}, status_code=200)
        response.set_cookie(cookie_name,cookie_id, path="/", expires=3600, samesite="Lax", secure=True)
        print(response)
        return response
    else:
        raise HTTPException(status_code=401, detail="Wrong Credentials received")




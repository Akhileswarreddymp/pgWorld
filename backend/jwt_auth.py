import jwt
from fastapi import FastAPI,HTTPException,APIRouter
import time
from decouple import config
from mongo_db import *
import hashlib
from models import *

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
    return token_resp(token)

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['exp'] >= time.time() else None
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
    if check_user(request):
        return signJWT(request.username)
    else:
        raise HTTPException(status_code=401, detail="Wrong Credentials received")




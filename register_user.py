from fastapi import FastAPI,HTTPException,APIRouter
import asyncio
import hashlib
from models import *
import pydantic
import pymongo


router = APIRouter()

# pydantic model for saving login details
class only_otp(pydantic.BaseModel):
    otp : str



@router.post('/verify_otp',tags=['Authentication'])
async def verify_otp(request : only_otp):
    print(type(request))
    request = dict(request)
    redis_client = redisclient()
    print("reg_otp",redis_client.redis_client.get('otp').decode())
    print("reg_send_otp",request)
    if str(request["otp"]) == str(redis_client.redis_client.get('otp').decode()):
        print("?????")
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Users"] 
        collection = db["users"]
        data = {
            "name" : redis_client.redis_client.get('name').decode(),
            "email" : redis_client.redis_client.get('temp_mail').decode(),
            "contact_number" : redis_client.redis_client.get('contact_number').decode(),
            "password" : redis_client.redis_client.get('temp_password'),
            "created_time" : datetime.datetime.now()
        }
        storing_into_mongo = collection.insert_one(data)

    #     mail = redis_client.redis_client.setex("email", 30000, redis_client.redis_client.get("temp_mail"))
    #     password = redis_client.redis_client.setex("password", 3000, redis_client.redis_client.get("temp_password"))
        return {"msg":"Registred Successfully"}
    else:
        raise HTTPException(status_code=401, detail="Wrong Credentials received")
    
    

# login
@router.post("/login", tags=['Authentication'])
def verification(request: verify_params):
    redis_client = redisclient()
    passwo = hashlib.md5(request.password.encode('utf-8')).hexdigest()
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    collection = client.get_database("Users").get_collection("users")
    print("passwo======>",passwo)
    result = collection.find_one({"email": request.username})
    print("db_email===>",result)
    if result.get("email") == request.username and result.get("password").decode() == passwo:
        return {"msg" : "Successfully Logged in "}
    else:
        raise HTTPException(status_code=401, detail="Wrong Credentials received")



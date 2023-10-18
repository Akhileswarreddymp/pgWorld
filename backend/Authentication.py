from fastapi import FastAPI,HTTPException,APIRouter
import asyncio
import hashlib
from models import *
from main import *
import pydantic
import pymongo
from mongo_db import *

router = APIRouter()

    

# login
@router.post("/login", tags=['Authentication'])
async def verification(request: verify_params):
    redis_client = redisclient()
    passwo = hashlib.md5(request.password.encode('utf-8')).hexdigest()
    # client = pymongo.MongoClient("mongodb://localhost:27017/")
    # collection = client.get_database("Users").get_collection("users")
    collection = await connect_collection("Users","users")
    print("passwo======>",passwo)
    result = collection.find_one({"email": request.username})
    print("db_email===>",result)
    if result.get("email") == request.username and result.get("password") == passwo:
        return {"msg" : "Successfully Logged in"}
    else:
        raise HTTPException(status_code=401, detail="Wrong Credentials received")

# Pydantic model for reset Password
class reset_pass(pydantic.BaseModel):
    username : str
    old_password : str
    new_password : str
    re_enter_password : str 

 # reset Password if user knows his old password   
@router.post('/resetpassword', tags=['Authentication'])
async def reset_password(request : reset_pass):
    collection = await connect_collection("Users","users")
    result = collection.find_one({"email": request.username})
    print("result==>",result)
    old_pass = hashlib.md5(request.old_password.encode('utf-8')).hexdigest()
    print("password is ==>",result.get("password"))
    print("new_pass==>",old_pass)
    if old_pass == result.get("password"):
        filter = {"_id":result.get("_id")}
        print("filter==>",filter)
        if request.new_password == request.re_enter_password:
            new_pass = hashlib.md5(request.new_password.encode('utf-8')).hexdigest()
            update_field = collection.update_one(filter,{'$set': {"password":new_pass}})
            return {"msg": "Password Updated Successfully"}
        else:
            raise HTTPException(status_code=401, detail="New Password and re entred password are not matched")
    else:
        raise HTTPException(status_code=401, detail="Received incorrect password")

# Pydantic model for reset Password
class forgot_pass(pydantic.BaseModel):
    username : str
    otp : str
    new_password : str
    re_enter_password : str 


@router.post('/forgotpassword',tags=['Authentication'])
async def forgot_password(request : forgot_pass):
    redis_client = redisclient()
    if request.otp == redis_client.redis_client.get("otp").decode():
        if request.new_password == request.re_enter_password:
            collection = await connect_collection("Users","users")
            result = collection.find_one({"email": request.username})
            filter = {"_id":result.get("_id")}
            new_pass = hashlib.md5(request.new_password.encode('utf-8')).hexdigest()
            update_field = collection.update_one(filter,{'$set': {"password":new_pass}})
            return {"msg": "Password Updated Successfully"}
        else:
            raise HTTPException(status_code=401, detail="New Password and re entred password are not matched")
    else:
        raise HTTPException(status_code=401, detail="Incorrect OTP")


